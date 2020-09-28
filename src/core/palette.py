"""Defines the Palette class"""

import pygame

class Palette:
    """Color palette for brush"""

    def __init__(self):
        self.colors = {
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "magenta": (255, 255, 0),
            "cyan": (0, 255, 255),
            "yellow": (255, 0, 255),
            "white": (255, 255, 255),
        }
        self.current_color = "black"
        self.rect = None

    def get_color_dict(self):
        """Get supported colors"""
        return self.colors

    def get_color_name_list(self):
        """Get color list sorted lexicographically"""
        return sorted(self.colors.keys())

    def set_current_color_by_name(self, color):
        """Set current color"""
        if color in self.colors:
            self.current_color = color
        else:
            print("Invalid color", color)

    def get_current_color_name(self):
        """Get current color name"""
        return self.current_color

    def get_current_color(self):
        """Get current color"""
        return self.colors[self.current_color]

    def draw(self, screen):
        """Draw pallette on canvas"""
        color = self.get_current_color()
        screen_rect = screen.get_rect()
        radius = 10
        margin = 10 + radius
        border_thickness = 2
        center = (screen_rect.width - margin, margin)
        # Border
        pygame.draw.circle(screen, (0, 0, 0), center, \
            radius + border_thickness)
        # Inner color
        self.rect = pygame.draw.circle(screen, color, center, radius)

    def next_color(self):
        """Set next color in the palette"""
        color_list = self.get_color_name_list()
        color_index = color_list.index(self.current_color)
        next_color_index = (color_index + 1) % len(color_list)
        self.set_current_color_by_name(color_list[next_color_index])
