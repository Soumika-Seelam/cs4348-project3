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
        print(f"Error: File '{file_name}' does not exist.")
        return None

    with open(file_name, "rb") as file:
        header_data = file.read(512)  # reads the first 512 bytes

        # then checks to see if the file has at least 512 bytes
        if len(header_data) < 512:
            print(f"Error: File '{file_name}' is too small to be a valid index file.")
            return None

        # next checks for the exact needed magic number in the first 8 bytes
        if header_data[:8] != b"4337PRJ3":
            print(f"Error: File '{file_name}' is not a valid index file (invalid magic number).")
            return None

        print(f"File '{file_name}' opened successfully.")
        return file_name

# defining the main function
def main():
    current_file = None
    while True:
        # commands/options that the user is given
        print("\nCommands: create, open, insert, search, quit")
        command = input("Enter command: ").strip().lower()

        # if loop that decides command
        if command == "create":
            file_name = input("Enter file name: ")
            create_index(file_name)
        elif command == "open":
            file_name = input("Enter file name: ")
            current_file = open_index(file_name)
        elif command == "quit":
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
