# Main module for the assistant bot handles user interaction and command execution
# Provides the main entry point for the assistant bot

from commands import create_commands, execute_command
from storage import load_data, save_data


def main():
    book, notes_book = load_data()
    commands = create_commands(book, notes_book)

    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")

    # Main loop for handling user commands
    while True:
        user_input = input("Enter a command: ").strip()

        if user_input.lower() in ["close", "exit"]:
            save_data(book, notes_book)
            print("Good bye!")
            break

        if user_input.lower() == "hello":
            print("How can I help you?")
            continue

        print(execute_command(user_input, commands))


if __name__ == "__main__":
    main()
