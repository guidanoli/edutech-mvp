from .action import Action

from pygame import surfarray

class Stroke(Action):
    """Represents a stroke"""

    def __init__(self, array):
        self.array = array

    def draw(self, canvas):
        """Overrides Action.draw"""
        surfarray.blit_array(canvas, self.array)
