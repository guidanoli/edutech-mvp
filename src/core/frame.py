class Frame:
    """Represents a frame"""

    def __init__(self, bgcolor):
        self.bgcolor = bgcolor
        self.actions = []

    def set_bgcolor(self, bgcolor):
        """Update background color"""
        self.bgcolor = bgcolor

    def add_action(self, action):
        """Add action"""
        self.actions.append(action)

    def remove_action(self):
        """Removes last action"""
        return self.actions.pop()

    def get_action_at(self, i):
        """Get action at index"""
        return self.actions[i]

    def get_action_count(self):
        """Get action count"""
        return len(self.actions)
    