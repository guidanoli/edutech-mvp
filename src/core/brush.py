from skimage.draw import line_aa

class Brush:
    """Class that represents the brush"""

    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.press_pos = (0, 0)

    def press(self, x, y):
        self.press_pos = (x, y)

    def move(self, img, x, y):
        old_x, old_y = self.press_pos
        row_map, column_map, intensity = line_aa(old_x, old_y, x, y)
        img[row_map, column_map] = intensity[:, None] * self.color
        self.press_pos = (x, y)