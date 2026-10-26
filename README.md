# Personal Assistant

Personal Assistant is a console application written in Python. It helps users manage contacts, birthdays, and personal notes.

## Features

- Add, edit, delete, and search contacts.
- Store phone numbers, emails, addresses, and birthdays.
- Validate phone numbers and email addresses.
- Show upcoming birthdays for a selected number of days and move weekend congratulations to Monday.
- Add, edit, delete, and search notes.
- Automatically save changes using `pickle`.
- Back up saved data and recover from a corrupted main data file.
- Choose and change the data storage directory.
- Reset saved data with confirmation and archive previous files.
- Display available commands and detailed instructions using `help`.

## Installation and Running

1. Download or clone the project from GitHub.
2. Make sure Python 3.10 or newer is installed.
3. Open a terminal in the project folder.
4. Install the package:

   ```bash
   python -m pip install .
   ```

5. Run the application from any directory:

   ```bash
   assistant
   ```

On the first run, the application will ask you to select a directory for storing your data.


## Project Structure

- `personal_assistant/` - Contains the application package.
- `personal_assistant/main.py` - Starts the application and handles user input.
- `personal_assistant/commands.py` - Stores available commands and executes them.
- `personal_assistant/handlers.py` - Contains functions for working with contacts and notes.
- `personal_assistant/models.py` - Contains classes for contacts, phone numbers, emails, addresses, and birthdays.
- `personal_assistant/notes.py` - Contains classes for creating and managing notes.
- `personal_assistant/config.py` - Manages application settings and the data storage directory.
- `personal_assistant/storage.py` - Saves, loads, and backs up contacts and notes using `pickle`.
- `pyproject.toml` - Defines package settings, dependencies, and the `assistant` command.
- `README.md` - Contains project information and instructions.

The application has a built-in help system with a hierarchical command structure.
Users can type `help` to see all available commands or `help add`, `help edit`, and other commands to get more detailed instructions.
Each command includes a description, required arguments, and an example of how to use it.

## Command Examples

```text
help
add contact Anna 0973443399
add contact email Anna anna@gmail.com
add contact address Anna Kyiv Ukraine
edit contact phone Anna 0973443399 0995533555
show contacts
search contact Anna
birthdays

add note Learn Python
show notes
search note Python
edit note 1 Learn Mathematics
delete note 1

exit
```

Use `help` to see available commands and `help add`, `help edit`, or `help show` to see more options.

## Data Storage

Contacts and notes are automatically saved to `assistant_data.pkl` in the selected directory.
A backup file, `assistant_data.pkl.bak`, is maintained for data recovery.

The application configuration is stored in `config.json` in the standard user configuration directory for the operating system.
This file stores the path to the selected data directory.