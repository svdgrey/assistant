# Handlers module provides functions to handle various commands for the assistant bot
# Each handler function is decorated with input_error to manage common input errors gracefully

from decorators import input_error
from models import Record


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), *args


@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    if record.birthday is None:
        return "Birthday not found."
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    if args:
        raise ValueError("Invalid command.")
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = ""
    for contact in upcoming:
        result += f"{contact['name']}: {contact['congratulation_date']}\n"
    return result.strip()


@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_email(email)
    return "Email added."


@input_error
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        return "Contact not found."

    if not address:
        return "Enter an address."

    record.add_address(address)
    return "Address added."


@input_error
def delete_contact(args, book):
    name = args[0]

    if book.find(name) is None:
        return "Contact not found."

    book.delete(name)
    return "Contact deleted."


@input_error
def change_email(args, book):
    name, email = args
    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_email(email)
    return "Email updated."


@input_error
def change_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        return "Contact not found."

    if not address:
        return "Enter an address."

    record.add_address(address)
    return "Address updated."

@input_error
def search_contacts(args, book):
    if not args:
        return "Enter a search query."

    query = " ".join(args).lower()
    found_contacts = []

    for record in book.data.values():
        # Search by contact name
        if query in record.name.value.lower():
            found_contacts.append(str(record))
            continue

        # Search by phone number
        for phone in record.phones:
            if query in phone.value:
                found_contacts.append(str(record))
                break
        else:
            # Search by email
            if record.email and query in record.email.value.lower():
                found_contacts.append(str(record))

    if not found_contacts:
        return "No contacts found."

    return "\n".join(found_contacts)



@input_error
def add_note(args, notes_book):
    if not args:
        return "Enter note text."

    text = " ".join(args)
    note_id = notes_book.add_note(text)
    return f"Note added with ID {note_id}."


@input_error
def show_notes(args, notes_book):
    return notes_book.show_all()


@input_error
def search_notes(args, notes_book):
    if not args:
        return "Enter a search query."

    query = " ".join(args)
    return notes_book.find_notes(query)


@input_error
def edit_note(args, notes_book):
    if len(args) < 2:
        return "Enter note ID and new text."

    note_id = int(args[0])
    text = " ".join(args[1:])

    if notes_book.edit_note(note_id, text):
        return "Note updated."

    return "Note not found."


@input_error
def delete_note(args, notes_book):
    if not args:
        return "Enter note ID."

    note_id = int(args[0])

    if notes_book.delete_note(note_id):
        return "Note deleted."

    return "Note not found."

