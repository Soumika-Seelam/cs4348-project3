# main function from which the project will be carried through
def main():
    while True:
        # just testing whether the project is working or not
        print("\nCommands: create, open, insert, search, quit")
        command = input("Enter command: ").strip().lower()

        if command == "quit":
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
