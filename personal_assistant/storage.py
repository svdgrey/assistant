# Storage module provides functions to save and load assistant data to and from a file
# It handles both contacts and notes data


import os
import shutil
import pickle
from pathlib import Path
from .models import AddressBook
from .notes import NotesBook
from datetime import datetime
from .config import get_data_directory, set_data_directory, validate_data_path

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


# Restore the main data file from a valid backup
def restore_backup(data_file, backup_file):
    result = read_data(backup_file)

    temp_file = data_file.with_suffix(".tmp")

    try:
        shutil.copy2(backup_file, temp_file)
        temp_file.replace(data_file)
    finally:
        try:
            temp_file.unlink(missing_ok=True)
        except OSError:
            pass

    return result


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
        result = restore_backup(data_file, backup_file)
        print("Main data file restored from backup.")
        return result

    except (OSError, pickle.UnpicklingError, EOFError,
            ValueError, AttributeError, ImportError, IndexError) as error:
        raise RuntimeError(
            f"Failed to load backup: {error}\n"
            "Data files have not been changed."
        ) from error



# Reset application data and preserve previous files
def reset_data(book, notes_book):
    data_file = get_data_file()
    backup_file = get_backup_file()

    # Generate a unique timestamp for archive files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Prepare archive file paths
    archives = []

    for file_path in (data_file, backup_file):
        if file_path.exists():
            archive_file = file_path.with_name(
                f"{file_path.name}.{timestamp}.save"
            )

            if archive_file.exists():
                raise FileExistsError(
                    f"Archive already exists: {archive_file}"
                )

            archives.append((file_path, archive_file))

    # Archive existing data files
    for file_path, archive_file in archives:
        shutil.copy2(file_path, archive_file)

    # Create and save an empty database
    empty_book = AddressBook()
    empty_notes = NotesBook()

    save_data(empty_book, empty_notes)

    # Remove the old backup after successful saving
    if backup_file.exists():
        backup_file.unlink()

    # Clear current objects only after successful saving
    book.data.clear()
    notes_book.notes.clear()
    notes_book.next_id = 1



# Copy application data to a new directory
def change_data_directory(user_path):
    old_directory = get_data_directory()
    new_directory = validate_data_path(user_path)

    if new_directory == old_directory:
        return "This directory is already in use."

    data_file = new_directory / DATA_FILENAME
    backup_file = new_directory / (DATA_FILENAME + BACKUP_SUFFIX)

    # Do not overwrite existing data
    if data_file.exists() or backup_file.exists():
        raise FileExistsError(
            "The selected directory already contains assistant data."
        )

    new_directory.mkdir(parents=True, exist_ok=True)

    # Copy existing files to the new directory
    for source_file in (get_data_file(), get_backup_file()):
        if source_file.exists():
            shutil.copy2(
                source_file,
                new_directory / source_file.name
            )

    # Update configuration only after successful copying
    set_data_directory(new_directory)

    return f"Data directory changed to: {new_directory}"