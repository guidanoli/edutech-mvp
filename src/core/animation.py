class Animation:
    """Represents an animation"""

    def __init__(self, fps):
        self.fps = fps
        self.frames = []

    def add_frame(self, frame):
        """Adds frame"""
        self.frames.append(frame)

    def get_frame_count(self):
        """Gets number of frames"""
        return len(self.frames)

    def get_frame_at(self, i):
        """Gets frame at index"""
        return self.frames[i]

    def remove_frame_at(self, i):
        """Remove frame at index"""
        return self.frames.pop(i)
