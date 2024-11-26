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
    if os.path.exists(file_name):
        overwrite = input(f"{file_name} already exists. Overwrite? (yes/no): ").lower()
        if overwrite != "yes":
            print("Aborted.")
            return
    with open(file_name, "wb") as file:
        header = Header()
        file.write(header.to_bytes())
    print(f"Index file '{file_name}' created successfully.")

# defining the main function
def main():
    while True:
        print("\nCommands: create, open, insert, search, quit")
        command = input("Enter command: ").strip().lower()

        if command == "create":
            file_name = input("Enter file name: ")
            create_index(file_name)
        elif command == "quit":
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
