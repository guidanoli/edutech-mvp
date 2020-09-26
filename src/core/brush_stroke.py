from .stroke import Stroke

class BrushStroke(Stroke):
    """Represents a brush stroke"""

    def __init__(self, array, color):
        super().__init__(array)
        self.color = color

    def get_color(self):
        """Get color"""
        return self.color
