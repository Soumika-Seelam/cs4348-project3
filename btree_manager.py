# importing the needed libraries
import os
import struct

# this header class is what decided the structure
class Header:
    def __init__(self):
        self.magic_number = b"4337PRJ3"
        self.root_block = 0
        self.next_block = 1

    def to_bytes(self):
        # making sure that the header fields will be in binary format
        data = struct.pack(">8sQQ", self.magic_number, self.root_block, self.next_block)
        return data.ljust(512, b'\x00')  # 512 bytes!
    
    @classmethod
    def from_bytes(cls, data):
        # Read the header from binary
        magic_number, root_block, next_block = struct.unpack(">8sQQ", data[:24])
        if magic_number != b"4337PRJ3":
            raise ValueError("Invalid magic number in the header")
        header = cls()
        header.magic_number = magic_number
        header.root_block = root_block
        header.next_block = next_block
        return header

# node class for the insert function
class Node:
    def __init__(self, block_id):
        self.block_id = block_id
        self.parent_id = 0
        self.key_count = 0
        self.keys = [0]*(2*10-1)
        self.values = [0]*(2*10-1)
        self.children = [0]*(2*10)

    def to_bytes(self):
        # here we serialize the Node to a binary format
        data = struct.pack(">QQQ", self.block_id, self.parent_id, self.key_count)
        data += struct.pack(f">{len(self.keys)}Q", *self.keys)
        data += struct.pack(f">{len(self.values)}Q", *self.values)
        data += struct.pack(f">{len(self.children)}Q", *self.children)
        return data.ljust(512, b'\x00')

    @classmethod
    def from_bytes(cls, data):
        # here we then deserialize the binary data into a Node object
        block_id, parent_id, key_count = struct.unpack(">QQQ", data[:24])
        keys = list(struct.unpack(f">{2 * 10 - 1}Q", data[24:24 + (2 * 10 - 1) * 8]))
        values = list(struct.unpack(f">{2 * 10 - 1}Q", data[24 + (2 * 10 - 1) * 8:24 + 2 * (2 * 10 - 1) * 8]))
        children = list(struct.unpack(f">{2 * 10}Q", data[24 + 2 * (2 * 10 - 1) * 8:24 + 2 * (2 * 10 - 1) * 8 + (2 * 10) * 8]))
        node = cls(block_id)
        node.parent_id = parent_id
        node.key_count = key_count
        node.keys = keys
        node.values = values
        node.children = children
        return node

# defining the function that will create the new index file
def create_index(file_name):
    # making sure that user knows they're not making an idx file (which they should!)
    if not file_name.endswith(".idx"):
        confirm = input(f"The file '{file_name}' does not have a .idx extension. Proceed anyway? (yes/no): ").lower()
        if confirm != "yes":
            print("Aborted.")
            return

    if os.path.exists(file_name):
        overwrite = input(f"{file_name} already exists. Overwrite? (yes/no): ").lower()
        if overwrite != "yes":
            print("Aborted.")
            return
    with open(file_name, "wb") as file:
        header = Header()
        file.write(header.to_bytes())
    print(f"Index file '{file_name}' created successfully.")

# function which checks if the file name is valid
def open_index(file_name):
    # checks whether that file actually exists
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' doesn't exist!")
        return None

    with open(file_name, "rb") as file:
        header_data = file.read(512)

        # then we check to see if the file has at least (the needed) 512 bytes
        if len(header_data) < 512:
            print(f"Error: File '{file_name}' is too small to be a valid index file.")
            return None

        # next checks for the exact needed magic number in the first 8 bytes
        if header_data[:8] != b"4337PRJ3":
            print(f"Error: File '{file_name}' is not a valid index file (invalid magic number).")
            return None

        print(f"File '{file_name}' opened successfully.")
        return file_name

# the insert function lets the user insert a key-value pair
def insert(file_name, key, value):
    with open(file_name, "r+b") as file:
        # reading the header to get root and next block information
        header_data = file.read(512)
        header = Header.from_bytes(header_data)

        if header.root_block == 0:
            # the tree is empty so we can create the root node
            root = Node(header.next_block)
            root.keys[0] = key
            root.values[0] = value
            root.key_count = 1

            # we then update the header to set the root block and then to increment next block ID
            header.root_block = root.block_id
            header.next_block += 1

            # we next write the updated header and root node to the file
            file.seek(0)
            file.write(header.to_bytes())
            file.seek(root.block_id * 512)
            file.write(root.to_bytes())
            print(f"Inserted key={key}, value={value} as the root node.")
        else:
            # we check that the tree is not empty and then insert into the right location
            insert_into_tree(file, header, header.root_block, key, value)

def read_block(file, block_id):
    # here we read the block
    file.seek(block_id * 512)
    return file.read(512)

def insert_into_tree(file, header, block_id, key, value):
    node_data = read_block(file, block_id)
    node = Node.from_bytes(node_data)

    # here we check if the key already exists
    if key in node.keys[:node.key_count]:
        print(f"Error: Key {key} already exists.")
        return
    
    if node.children[0] == 0:
        # leaf node which inserts the key and the value
        insert_into_leaf(node, key, value)
        file.seek(node.block_id * 512)
        file.write(node.to_bytes())
        print(f"Inserted key={key}, value={value} into leaf node.")
    else:
        # the internal node which decides what is the correct child
        child_index = find_child_index(node, key)
        child_block = node.children[child_index]
        insert_into_tree(file, header, child_block, key, value)

def insert_into_leaf(node, key, value):
    # here we insert the key and value pair into the node's position that is sorted
    index = 0
    while index < node.key_count and key > node.keys[index]:
        index += 1
    node.keys.insert(index, key)
    node.values.insert(index, value)
    node.key_count += 1

def find_child_index(node, key):
    # we then find the correct child pointer for the key
    for i in range(node.key_count):
        if key < node.keys[i]:
            return i
    return node.key_count

# defining the main function
def main():
    current_file = None
    while True:
        # commands/options that the user is given
        print("\nCommands: create, open, insert, search, quit")
        command = input("Enter command: ").strip().lower()

        # if loop that decides command
        if command == "create":
            file_name = input("Enter name of the new file: ")
            create_index(file_name)
        elif command == "open":
            file_name = input("Enter file of file you'd like to open: ")
            current_file = open_index(file_name)
        elif command == "insert":
            if not current_file:
                print("Error: No file is currently open.")
                continue
            key = int(input("Enter key (unsigned integer): "))
            value = int(input("Enter value (unsigned integer): "))
            insert(current_file, key, value)
        elif command == "quit":
            break
        else:
            print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
