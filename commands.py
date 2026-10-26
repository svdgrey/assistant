# Commands module defines the structure of available commands for the assistant bot
# It includes command descriptions, argument requirements, and associated handlers

import handlers
import pickle
from storage import save_data

# Function to create the command structure for the assistant bot
# It takes the address book and notes book as arguments and returns a dictionary of commands
def create_commands(book, notes_book):
    return {
        "add": {
            "description": "Add new information",
            "commands": {
                "contact": {
                    "description": "Add a contact",
                    "handler": handlers.add_contact,
                    "autosave": True,
                    "data": book,
                    "args": "<name> <phone>",
                    "min_args": 2,
                    "example": "add contact John 0973333333",
                    "commands": {
                        "email": {
                            "description": "Add an email to a contact",
                            "handler": handlers.add_email,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <email>",
                            "min_args": 2,
                            "example": "add contact email John john@gmail.com",
                        },
                        "address": {
                            "description": "Add a contact address",
                            "handler": handlers.add_address,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <address>",
                            "min_args": 2,
                            "example": "add contact address John Kyiv Ukraine",
                        },
                        "phone": {
                            "description": "Add a phone number",
                            "handler": handlers.add_contact,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <phone>",
                            "min_args": 2,
                            "example": "add contact phone John 0984444444",
                        },
                        "birthday": {
                            "description": "Add a birthday to a contact",
                            "handler": handlers.add_birthday,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <DD.MM.YYYY>",
                            "min_args": 2,
                            "example": "add contact birthday John 15.05.1995",
                        },
                    },
                },
                "note": {
                    "description": "Create a new note",
                    "handler": handlers.add_note,
                    "autosave": True,
                    "data": notes_book,
                    "args": "<text>",
                    "min_args": 1,
                    "example": "add note Learn Python",
                },
            },
        },
        "edit": {
            "description": "Edit existing information",
            "commands": {
                "contact": {
                    "description": "Edit contact fields",
                    "commands": {
                        "phone": {
                            "description": "Change a phone number",
                            "handler": handlers.change_contact,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <old_phone> <new_phone>",
                            "min_args": 3,
                            "example": "edit contact phone John 0973333333 0995555555",
                        },
                        "email": {
                            "description": "Change contact email",
                            "handler": handlers.change_email,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <new_email>",
                            "min_args": 2,
                            "example": "edit contact email John john@gmail.com",
                        },
                        "address": {
                            "description": "Change contact address",
                            "handler": handlers.change_address,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <address>",
                            "min_args": 2,
                            "example": "edit contact address John Lviv Ukraine",
                        },
                        "birthday": {
                            "description": "Change contact birthday",
                            "handler": handlers.add_birthday,
                            "autosave": True,
                            "data": book,
                            "args": "<name> <DD.MM.YYYY>",
                            "min_args": 2,
                            "example": "edit contact birthday John 15.05.1995",
                        },
                    },
                },
                "note": {
                    "description": "Edit an existing note",
                    "handler": handlers.edit_note,
                    "autosave": True,
                    "data": notes_book,
                    "args": "<id> <new_text>",
                    "min_args": 2,
                    "example": "edit note 1 Learn OOP",
                },
            },
        },
        "delete": {
            "description": "Delete saved information",
            "commands": {
                "contact": {
                    "description": "Delete a contact",
                    "handler": handlers.delete_contact,
                    "autosave": True,
                    "data": book,
                    "args": "<name>",
                    "min_args": 1,
                    "example": "delete contact John",
                },
                "note": {
                    "description": "Delete a note",
                    "handler": handlers.delete_note,
                    "autosave": True,
                    "data": notes_book,
                    "args": "<id>",
                    "min_args": 1,
                    "example": "delete note 1",
                },
            },
        },
        "search": {
            "description": "Search saved information",
            "commands": {
                "contact": {
                    "description": "Search contacts",
                    "handler": handlers.search_contacts,
                    "data": book,
                    "args": "<query>",
                    "min_args": 1,
                    "example": "search contact John",
                },
                "note": {
                    "description": "Search notes",
                    "handler": handlers.search_notes,
                    "data": notes_book,
                    "args": "<query>",
                    "min_args": 1,
                    "example": "search note Python",
                },
            },
        },
        "show": {
            "description": "Display saved information",
            "commands": {
                "contacts": {
                    "description": "Show all contacts",
                    "handler": handlers.show_all,
                    "data": book,
                    "args": "",
                    "min_args": 0,
                    "example": "show contacts",
                },
                "notes": {
                    "description": "Show all notes",
                    "handler": handlers.show_notes,
                    "data": notes_book,
                    "args": "",
                    "min_args": 0,
                    "example": "show notes",
                },
                "contact": {
                    "description": "Show contact information",
                    "commands": {
                        "phone": {
                            "description": "Show contact phone numbers",
                            "handler": handlers.show_phone,
                            "data": book,
                            "args": "<name>",
                            "min_args": 1,
                            "example": "show contact phone John",
                        },
                        "birthday": {
                            "description": "Show contact birthday",
                            "handler": handlers.show_birthday,
                            "data": book,
                            "args": "<name>",
                            "min_args": 1,
                            "example": "show contact birthday John",
                        },
                    },
                },
            },
        },
        "birthdays": {
            "description": "Show birthdays within the specified number of days",
            "handler": handlers.birthdays,
            "data": book,
            "args": "[days] (default: 7)",
            "min_args": 0,
            "example": "birthdays 14",
        },
        "reset": {
            "description": "Reset all contacts and notes",
            "args": "",
            "example": "reset",
            "min_args": 0,
        },
    }

# Function to display help information for available commands
# It takes the commands dictionary and an optional path string to indicate the current command context
def show_help(commands, path=""):
    if "commands" in commands or "handler" not in commands:
        available = commands.get("commands", commands)
        title = f"Available commands for '{path}':" if path else "Available commands:"
        lines = [title]

        if "handler" in commands:
            lines.append(f"  {path} {commands['args']}")
            lines.append(f"  Example: {commands['example']}")
            lines.append("")

        for name, command in available.items():
            lines.append(f"  {name:<12} - {command['description']}")

        return "\n".join(lines)

    return (
        f"Description: {commands['description']}\n"
        f"Arguments: {commands['args'] or 'None'}\n"
        f"Example: {commands['example']}"
    )


# Find a command and return its data and position
def find_command(words, commands):
    current = commands
    position = 0

    while position < len(words):
        if "commands" in current:
            available = current["commands"]
        elif "description" not in current:
            available = current
        else:
            break

        word = words[position].lower()

        if word not in available:
            break

        current = available[word]
        position += 1

    return current, position


# Function to get help information for a specific command based on user input words
# It uses the find_command function to locate the command and then displays its help
def get_help(words, commands):
    current, position = find_command(words, commands)
    path = " ".join(words[:position])

    if position != len(words):
        return "Unknown command.\n" + show_help(current, path)

    return show_help(current, path)


# Execute a command and handle errors
def call_handler(command, args, book, notes_book):
    try:
        result = command["handler"](args, command["data"])

    except (KeyError, ValueError, IndexError) as error:
        message = str(error)

        if isinstance(error, KeyError):
            message = message.strip("'")

        return message or "Enter the argument for the command."

    if command.get("autosave", False):
        try:
            save_data(book, notes_book)
        except FileNotFoundError as error:
            return (
                f"{result}\n"
                f"Warning: Data directory not found: {error}\n"
                "Changes are not saved. Please restore the data directory."
            )

        except (OSError, pickle.PickleError) as error:
            return f"{result}\nWarning: Data saving failed: {error}"

    return result


# Function to execute a command based on user input
# It parses the input, finds the corresponding command, checks argument requirements, and calls the handler
def execute_command(user_input, commands, book, notes_book):
    words = user_input.split()

    if not words:
        return show_help(commands)

    if words[0].lower() == "help":
        return get_help(words[1:], commands)

    current, position = find_command(words, commands)
    path = " ".join(words[:position])

    if "handler" not in current:
        return show_help(current, path)

    args = words[position:]

    if len(args) < current["min_args"]:
        return "Not enough arguments.\n" + show_help(current, path)

    return call_handler(current, args, book, notes_book)
