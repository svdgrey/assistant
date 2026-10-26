# Storage module provides functions to save and load assistant data to and from a file
# It handles both contacts and notes data

import os
import shutil
import pickle
from pathlib import Path
from models import AddressBook
from notes import NotesBook
from config import get_data_directory


DATA_FILENAME = "assistant_data.pkl"
BACKUP_SUFFIX = ".bak"


# Get the path to the application data file
def get_data_file():
    return get_data_directory() / DATA_FILENAME

# Return the path to the application data backup file
def get_backup_file():
    return get_data_directory() / (DATA_FILENAME + BACKUP_SUFFIX)



# Create a backup file only if the main data file is valid
def create_backup(data_file, backup_file):
    if not data_file.exists():
        return

    try:
        read_data(data_file)
    except (OSError, pickle.UnpicklingError, EOFError,
            ValueError, AttributeError, ImportError, IndexError):
        # Keep the existing backup unchanged
        return

    temp_backup = backup_file.with_suffix(".tmp")

    try:
        shutil.copy2(data_file, temp_backup)
        temp_backup.replace(backup_file)
    finally:
        try:
            temp_backup.unlink(missing_ok=True)
        except OSError:
            pass



# Saves the address book and notes book to a file
# also creates a backup of the existing data file to prevent data loss
# Parameters:
# - book: AddressBook instance containing contact records
# - notes_book: NotesBook instance containing notes
def save_data(book, notes_book):
    data_file = get_data_file()
    backup_file = get_backup_file()
    temp_file = data_file.with_suffix(".tmp")

    data = {
        "contacts": book,
        "notes": notes_book,
    }

    try:
        # Write new data to a temporary file
        with open(temp_file, "wb") as file:
            pickle.dump(data, file)
            file.flush()
            os.fsync(file.fileno())

        create_backup(data_file, backup_file)

        # Replace the main file after successful writing
        temp_file.replace(data_file)

    finally:
        try:
            temp_file.unlink(missing_ok=True)
        except OSError:
            pass


# Read and validate saved contacts and notes
def read_data(file_path):
    with open(file_path, "rb") as file:
        data = pickle.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid data format.")

    if not isinstance(data.get("contacts"), AddressBook):
        raise ValueError("Invalid contacts data.")

    if not isinstance(data.get("notes"), NotesBook):
        raise ValueError("Invalid notes data.")

    return data["contacts"], data["notes"]


# Loads saved data or restore it from a backup
# Returns a tuple containing:
# - AddressBook instance with contact records
# - NotesBook instance with notes
# If the file does not exist, returns empty AddressBook and NotesBook instances
def load_data():
    data_file = get_data_file()
    backup_file = get_backup_file()

    if not data_file.exists() and not backup_file.exists():
        return AddressBook(), NotesBook()

    try:
        return read_data(data_file)

    except (OSError, pickle.UnpicklingError, EOFError,
            ValueError, AttributeError, ImportError, IndexError) as error:
        print(f"Failed to load main data: {error}")

    try:
        result = read_data(backup_file)
        print("Data loaded from backup.")
        return result

    except (OSError, pickle.UnpicklingError, EOFError,
            ValueError, AttributeError, ImportError, IndexError) as error:
        raise RuntimeError(
            f"Failed to load backup: {error}\n"
            "Data files have not been changed."
        ) from error

