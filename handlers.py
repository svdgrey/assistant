# Handlers module provides functions to handle various commands for the assistant bot
from models import Record

# Function to parse user input into command and arguments
def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.lower(), *args

# Handler function to add a new contact to the address book
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

# Handler function to change a contact's phone number
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

# Handler function to show a contact's phone numbers
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    return ", ".join(phone.value for phone in record.phones)


# Handler function to show all contacts
def show_all(args, book):
    if not book.data:
        return "No contacts found."

    return "\n".join(str(record) for record in book.data.values())

# Handler function to add a birthday to a contact
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."


# Handler function to show a contact's birthday
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Enter user name.")
    record = book.find(args[0])
    if record is None:
        raise KeyError("Contact not found.")
    if record.birthday is None:
        return "Birthday not found."
    return record.birthday.value.strftime("%d.%m.%Y")


# Handler function to show upcoming birthdays within the specified number of days
def birthdays(args, book):
    if len(args) > 1:
        raise ValueError("Enter the number of days.")

    days = 7

    if args:
        days = int(args[0])

    if days < 0:
        raise ValueError("Number of days cannot be negative.")

    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return "No upcoming birthdays."

    result = ""
    for contact in upcoming:
        result += f"{contact['name']}: {contact['congratulation_date']}\n"

    return result.strip()


# Handler function to add an email to a contact
def add_email(args, book):
    name, email = args
    record = book.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    record.add_email(email)
    return "Email added."


# Handler function to add an address to a contact
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    if not address:
        raise ValueError("Enter an address.")

    record.add_address(address)
    return "Address added."

# Handler function to delete a contact
def delete_contact(args, book):
    name = args[0]

    if book.find(name) is None:
        raise KeyError("Contact not found.")

    book.delete(name)
    return "Contact deleted."


# Handler function to change a contact's email
def change_email(args, book):
    name, email = args
    record = book.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    record.add_email(email)
    return "Email updated."

# Handler function to change a contact's address
def change_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)

    if record is None:
        raise KeyError("Contact not found.")

    if not address:
        raise ValueError("Enter an address.")

    record.add_address(address)
    return "Address updated."

# Handler function to search contacts
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


# Handler function to add a note
def add_note(args, notes_book):
    if not args:
        raise ValueError("Enter note text.")

    text = " ".join(args)
    note_id = notes_book.add_note(text)
    return f"Note added with ID {note_id}."


# Handler function to show all notes
def show_notes(args, notes_book):
    return notes_book.show_all()


# Handler function to search notes
def search_notes(args, notes_book):
    if not args:
        return "Enter a search query."

    query = " ".join(args)
    return notes_book.find_notes(query)


# Handler function to edit a note
def edit_note(args, notes_book):
    if len(args) < 2:
        raise ValueError("Enter note ID and new text.")

    note_id = int(args[0])
    text = " ".join(args[1:])

    if notes_book.edit_note(note_id, text):
        return "Note updated."

    raise ValueError("Note not found.")


# Handler function to delete a note
def delete_note(args, notes_book):
    if not args:
        raise ValueError("Enter note ID.")

    note_id = int(args[0])

    if notes_book.delete_note(note_id):
        return "Note deleted."

    raise ValueError("Note not found.")

