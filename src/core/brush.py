from skimage.draw import line_aa

class Brush:
    """Class that represents the brush"""

    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.press_pos = (0, 0)

    def set_color(self, color):
        """Set color"""
        self.color = color

    def press(self, x, y):
        """Started pressing brush against canvas"""
        self.press_pos = (x, y)

    def move(self, img, x, y):
        """Moving brush through canvas"""
        old_x, old_y = self.press_pos
        row_map, column_map, _ = line_aa(old_x, old_y, x, y)
        img[row_map, column_map] = self.color
        self.press_pos = (x, y)
