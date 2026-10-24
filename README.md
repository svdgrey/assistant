# Personal Assistant

Personal Assistant is a console application written in Python. It helps users manage contacts, birthdays, and personal notes.

## Features

- Add, edit, delete, and search contacts.
- Store phone numbers, emails, addresses, and birthdays.
- Validate phone numbers and email addresses.
- Show upcoming birthdays and move weekend congratulations to Monday.
- Add, edit, delete, and search notes.
- Save and load data using `pickle`.
- Display available commands using `help`.

## Installation and Running

1. Download or clone the project from GitHub.
2. Make sure Python 3 is installed.
3. Open a terminal in the project folder.
4. Run the application:

```bash
python main.py
```
No additional libraries are required.

## Project Structure

- `main.py` - Starts the application and handles user input.
- `commands.py` - Stores available commands and executes them.
- `handlers.py` - Contains functions for working with contacts and notes.
- `models.py` - Contains classes for contacts, phone numbers, emails, addresses, and birthdays.
- `notes.py` - Contains classes for creating and managing notes.
- `decorators.py` - Handles common user input errors.
- `storage.py` - Saves and loads contacts and notes using `pickle`.
- `README.md` - Contains project information and instructions.

Has its own built-in help system with a hierarchical command structure.
Users can type help to see all available commands or help add, help edit, and other commands to get more detailed instructions.
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

Contacts and notes are automatically saved to the `assistant_data.pkl` file in the user's home directory when the application is closed with `exit` or `close`.
