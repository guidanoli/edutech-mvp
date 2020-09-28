from pygame import surfarray
import numpy as np

class Frame:
    """Represents a frame"""

    def __init__(self, width, height, bgcolor):
        self.bgcolor = bgcolor
        self.img = np.zeros((width, height, 3), np.int8)
        self.clean()

    def get_image(self):
        """Get frame image"""
        return self.img

    def clean(self):
        """Clean frame"""
        self.img[:,:] = self.bgcolor

    def draw(self, canvas):
        """Draw on canvas"""
        surfarray.blit_array(canvas, self.img)

    def serialize(self, file):
        """Serialize to binary file"""
        np.savez_compressed(file, **self.__dict__)

    @staticmethod
    def deserialize(file):
        """Deserialize from binary file"""
        data = np.load(file + ".npz")
        frame = Frame.__new__(Frame)
        for key, value in data.items():
            setattr(frame, key, value)
        return frame
