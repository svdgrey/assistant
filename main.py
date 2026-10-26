# Main module for the assistant bot handles user interaction and command execution
# Provides the main entry point for the assistant bot

import pickle

from commands import create_commands, execute_command
from models import AddressBook
from notes import NotesBook
from storage import load_data, reset_data, get_data_file


# Ask the user to confirm a data reset
def confirm_reset():
    while True:
        answer = input("Reset all data? [yes/No]: ").strip().lower()

        if answer == "yes":
            return True

        if answer in ("no", ""):
            return False

        print("Please enter yes or no.")


def main():

    try:
        book, notes_book = load_data()
    except (RuntimeError, OSError) as error:
        print(f"Failed to load data: {error}")

        if not confirm_reset():
            print("Reset cancelled.")
            return

        book = AddressBook()
        notes_book = NotesBook()

        try:
            reset_data(book, notes_book)
        except (OSError, pickle.PickleError) as error:
            print(f"Failed to reset data: {error}")
            return

        print("Data reset successfully.")

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

            if user_input.lower() == "reset":
                if confirm_reset():
                    try:
                        reset_data(book, notes_book)
                        print("Data reset successfully.")
                    except OSError as error:
                        print(f"Failed to reset data: {error}")
                else:
                    print("Reset cancelled.")

                continue

            print(execute_command(user_input, commands, book, notes_book))

    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")


if __name__ == "__main__":
    main()
