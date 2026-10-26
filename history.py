

# Store actions for undo and redo
class CommandHistory:
    def __init__(self, max_size=10):
        self.undo_stack = []
        self.redo_stack = []
        self.max_size = max_size

    # Add a completed action to history
    def add(self, undo_action, redo_action):
        self.undo_stack.append((undo_action, redo_action))
        self.redo_stack.clear()

        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)

    # Undo the last action
    def undo(self):
        if not self.undo_stack:
            return "Nothing to undo."

        undo_action, redo_action = self.undo_stack[-1]
        undo_action()

        self.undo_stack.pop()
        self.redo_stack.append((undo_action, redo_action))

        return "Last action undone."

    # Redo the last undone action
    def redo(self):
        if not self.redo_stack:
            return "Nothing to redo."

        undo_action, redo_action = self.redo_stack[-1]
        redo_action()

        self.redo_stack.pop()
        self.undo_stack.append((undo_action, redo_action))

        return "Last action restored."
