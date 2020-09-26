import pygame
import numpy
from pygame.locals import *

import core

def main():
    """Runs canvas code"""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption('Canvas')

    # Prepare brush
    brush_size = 1
    brush_color = (0, 0, 0)
    brush = core.Brush(brush_size, brush_color)

    # Prepare animation
    animation = core.Animation()
    screen_size = screen.get_size()
    bgcolor = (255, 255, 255) # White
    animation.add_frame(core.Frame(*screen_size, bgcolor))

    mouse_down = False
    playing = False

    # Main loop
    going = True
    while going:

        frame = animation.get_current_frame()
        img = frame.get_image()
        pos = pygame.mouse.get_pos()

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
                brush.press(*pos)
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
                brush.move(img, *pos)

        if mouse_down:
            brush.move(img, *pos)

        animation.update()
        animation.draw(screen)
        pygame.display.flip()

        if playing:
            animation.next_frame()

if __name__ == '__main__':
    main()
