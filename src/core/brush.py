"""Defines the Brush class"""

from skimage.draw import line, disk

class Brush:
    """Class that represents the brush"""

    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.press_pos = (0, 0)

    def get_size(self):
        """Get size"""
        return self.size

    def set_size(self, size):
        """Set size"""
        self.size = size

    def set_color(self, color):
        """Set color"""
        self.color = color

    def press(self, x, y):
        """Started pressing brush against canvas"""
        self.press_pos = (x, y)

    def move(self, img, x, y):
        """Moving brush through canvas"""
        old_x, old_y = self.press_pos
        for c_x, c_y in zip(*disk((old_x, old_y), self.size, shape=img.shape)):
            end_x = min(x + (c_x - old_x), img.shape[0] - 1)
            end_y = min(y + (c_y - old_y), img.shape[1] - 1)
            row_map, column_map = line(c_x, c_y, end_x, end_y)
            img[row_map, column_map] = self.color
        self.press_pos = (x, y)
