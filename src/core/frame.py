from pygame import surfarray
import numpy as np

class Frame:
    """Represents a frame"""

    def __init__(self, width, height, bgcolor):
        self.bgcolor = bgcolor
        self.img = np.zeros((width, height, 3), np.int8)
        self.img[:,:] = bgcolor

    def get_image(self):
        """Get frame image"""
        return self.img

    def draw(self, canvas):
        """Draw on canvas"""
        surfarray.blit_array(canvas, self.img)
        