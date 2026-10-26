# Main module for the assistant bot handles user interaction and command execution
# Provides the main entry point for the assistant bot

import pickle

from commands import create_commands, execute_command
from storage import load_data, save_data, get_data_file


def main():

    try:
        book, notes_book = load_data()
    except (RuntimeError, OSError) as error:
        print(f"Failed to load data: {error}")
        return

    commands = create_commands(book, notes_book)

    print("Welcome to the assistant bot!")
    print(f"Data file: {get_data_file()}")
    print("Type 'help' to see available commands.")

    # Main loop for handling user commands
    try:
        while True:
            user_input = input("Enter a command: ").strip()

            if user_input.lower() in ["exit", "close"]:
                print("Good bye!")
                break

            if user_input.lower() == "hello":
                print("How can I help you?")
                continue

            print(execute_command(user_input, commands, book, notes_book))

    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")


if __name__ == "__main__":
    main()
