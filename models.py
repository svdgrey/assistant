from collections import UserDict
from datetime import datetime, date, timedelta
import email
import re


# Base class for all fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Stores the contact's name
class Name(Field):
    pass

# Store and validate a 10-digit phone number.
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)



# Store and validate an email address.
class Email(Field):
    def __init__(self, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid email address.")

        super().__init__(value)


# Store and Address.
class Address(Field):
    pass


# Store and validate a birthday in DD.MM.YYYY format.
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            if birthday.strftime("%d.%m.%Y") != value:
                raise ValueError
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(birthday)


# Record class represents a contact record in the address book
# It contains the contact's name, phones, birthday, email, and address
# Provides methods to add, remove, and edit phones, as well as add birthday, email, and address
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if not found_phone:
            raise ValueError("Phone number not found.")
        new_phone = Phone(new_phone)
        found_phone.value = new_phone.value

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)


    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        email = self.email.value if self.email else "Not specified"
        address = self.address.value if self.address else "Not specified"

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"email: {email}, "
            f"address: {address}"
        )

# AddressBook class represents the address book containing all contact records
# It provides methods to add, find, delete records and get upcoming birthdays
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # Adjust February 29 birthdays to March 1 in non-leap years.
    def adjust_leap_day_birthday(self, date_of_birth: date, year: int) -> date:
        try:
            return date_of_birth.replace(year=year)
        except ValueError:
            return date_of_birth.replace(year=year, month=3, day=1)

    # Find the next birthday, adjusting February 29 if necessary.
    def get_next_birthday(self, date_of_birth: date, today: date) -> date:
        next_birthday = self.adjust_leap_day_birthday(date_of_birth, today.year)

        if next_birthday < today:
            next_birthday = self.adjust_leap_day_birthday(date_of_birth, today.year + 1)

        return next_birthday

    # Get birthdays within the next 7 days, including today.
    # Move weekend congratulations to Monday.
    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            date_of_birth = record.birthday.value.date()
            next_birthday = self.get_next_birthday(date_of_birth, today)

            if 0 <= (next_birthday - today).days <= 7:
                weekday = next_birthday.weekday()

                # Move weekend birthdays to Monday
                if weekday >= 5:
                    next_birthday += timedelta(days=7 - weekday)

                congratulation_date = next_birthday

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return upcoming_birthdays
