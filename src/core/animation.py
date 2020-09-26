class Animation:
    """Represents an animation"""

    def __init__(self, fps=2):
        self.fps = fps
        self.current_frame = 0
        self.frames = []

    def get_fps(self):
        """Get frames per second"""
        return self.fps

    def add_frame(self, frame):
        """Adds frame"""
        self.frames.append(frame)

    def get_frame_count(self):
        """Gets number of frames"""
        return len(self.frames)
    
    def prev_frame(self):
        """Set the current frame to the previous frame"""
        self.set_current_frame((self.current_frame - 1) % self.get_frame_count())

    def next_frame(self):
        """Set the current frame to the next frame"""
        self.set_current_frame((self.current_frame + 1) % self.get_frame_count())

    def get_current_frame(self):
        """Get current frame"""
        return self.get_frame_at(self.current_frame)

    def set_current_frame(self, f):
        """Set current frame"""
        self.current_frame = f

    def get_current_frame_index(self):
        """Get current frame index"""
        return self.current_frame

    def get_frame_at(self, i):
        """Gets frame at index"""
        return self.frames[i]

    def remove_frame_at(self, i):
        """Remove frame at index"""
        return self.frames.pop(i)

    def update(self):
        """Updates animation"""

    def draw(self, screen):
        """Draws animation"""
        self.get_current_frame().draw(screen)
