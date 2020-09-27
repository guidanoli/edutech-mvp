from skimage.draw import line, circle

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
        for c_x, c_y in zip(*circle(old_x, old_y, self.size, shape=img.shape)):
            row_map, column_map = line(c_x, c_y, x + (c_x - old_x), y + (c_y - old_y))
            img[row_map, column_map] = self.color
        self.press_pos = (x, y)
