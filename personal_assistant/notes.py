# Notes module provides classes to manage notes and a notes book
# It provides Note and NotesBook classes to create, edit, delete, and search notes

# Note class represents a single note with text content
# It provides methods to initialize and display the note text 
class Note:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


# NotesBook class represents a collection of notes
# It provides methods to add, show, find, edit, and delete notes
class NotesBook:
    def __init__(self):
        self.notes = {}
        self.next_id = 1

    def add_note(self, text):
        note_id = self.next_id
        self.notes[note_id] = Note(text)
        self.next_id += 1
        return note_id

    def show_all(self):
        if not self.notes:
            return "No notes found."

        result = ""
        for note_id, note in self.notes.items():
            result += f"{note_id}: {note}\n"

        return result.strip()

    def find_notes(self, query):
        result = ""

        for note_id, note in self.notes.items():
            if query.lower() in note.text.lower():
                result += f"{note_id}: {note}\n"

        return result.strip() or "No notes found."

    def edit_note(self, note_id, text):
        if note_id not in self.notes:
            return False

        self.notes[note_id].text = text
        return True

    def delete_note(self, note_id):
        if note_id not in self.notes:
            return False

        del self.notes[note_id]
        return True

