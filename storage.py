# Storage module provides functions to save and load assistant data to and from a file
# It handles both contacts and notes data


import pickle
from pathlib import Path

from models import AddressBook
from notes import NotesBook


DATA_FILE = Path.home() / "assistant_data.pkl"

# Saves the address book and notes book to a file
# Parameters:
# - book: AddressBook instance containing contact records
# - notes_book: NotesBook instance containing notes
def save_data(book, notes_book):
    data = {
        "contacts": book,
        "notes": notes_book
    }

    with open(DATA_FILE, "wb") as file:
        pickle.dump(data, file)


# Loads the address book and notes book from a file
# Returns a tuple containing:
# - AddressBook instance with contact records
# - NotesBook instance with notes
# If the file does not exist, returns empty AddressBook and NotesBook instances
def load_data():
    try:
        with open(DATA_FILE, "rb") as file:
            data = pickle.load(file)

        return data["contacts"], data["notes"]

    except FileNotFoundError:
        return AddressBook(), NotesBook()

