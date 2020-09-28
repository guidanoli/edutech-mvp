from .frame import Frame
from pathlib import Path
import json

class Animation:
    """Represents an animation"""

    def __init__(self, fps):
        self.fps = fps
        self.current_frame = 0
        self.frames = []

    def get_fps(self):
        """Get frames per second"""
        return self.fps

    def set_fps(self, fps):
        """Set frames per second"""
        self.fps = fps

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

    def set_current_frame(self, frame):
        """Set current frame"""
        self.current_frame = frame

    def get_current_frame_index(self):
        """Get current frame index"""
        return self.current_frame

    def get_frame_at(self, i):
        """Gets frame at index"""
        return self.frames[i]

    def remove_frame_at(self, i):
        """Remove frame at index
        Assumes there are at least two frames
        """
        self.frames.pop(i)
        if self.current_frame == i:
            self.set_current_frame(max(0, i-1))

    def update(self):
        """Updates animation"""

    def draw(self, screen):
        """Draws animation"""
        self.get_current_frame().draw(screen)

    @staticmethod
    def _get_project_info_path(prj_folder):
        """Get project info file path"""
        return Path(prj_folder) / "project.json"
    
    @staticmethod
    def _get_frame_file_path(prj_folder, frame_index):
        """Get frame file path"""
        return Path(prj_folder) / f"frame_{frame_index}"

    def serialize(self, prj_folder):
        """Serialize animation to project folder"""
        prj_info = self.__dict__.copy()
        prj_info.pop("frames")
        prj_info["frame_count"] = self.get_frame_count()
        prj_info_filepath = Animation._get_project_info_path(prj_folder)
        with open(prj_info_filepath, 'w') as prj_info_file:
            prj_info_file.write(json.dumps(prj_info,
                indent=4, sort_keys=True))
        for i, frame in enumerate(self.frames):
            frames_filepath = Animation._get_frame_file_path(prj_folder, i)
            frame.serialize(str(frames_filepath))

    @staticmethod
    def deserialize(prj_folder):
        """Deserialize animation from project folder"""
        animation = Animation.__new__(Animation)
        prj_info_filepath = Animation._get_project_info_path(prj_folder)
        with open(prj_info_filepath, 'r') as prj_info_file:
            data = json.load(prj_info_file)
            frame_count = data.pop('frame_count')
            for key, value in data.items():
                setattr(animation, key, value)
        animation.frames = []
        for i in range(frame_count):
            frame_filepath = Animation._get_frame_file_path(prj_folder, i)
            frame = Frame.deserialize(str(frame_filepath))
            animation.frames.append(frame)
        return animation
