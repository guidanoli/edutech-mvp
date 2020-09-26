import pygame
import numpy
from pygame.locals import *

import core

import os

if not pygame.font: print('Warning, fonts disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, '..', 'data')

def load_image(name, colorkey=None):
    """Loads image and returns image and its rectangle"""
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        raise SystemExit(f"Cannot load image: {fullname}") from err
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class NextButton(pygame.sprite.Sprite):
    """Button that goes to the next frame"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("next.gif", -1)
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.bottom = rect.height - 10
        self.rect.right = rect.width - 10

class PrevButton(pygame.sprite.Sprite):
    """Button that goes to the previous frame"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("prev.gif", -1)
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.bottom = rect.height - 10
        self.rect.left = 10

class PlayStopButton(pygame.sprite.Sprite):
    """Button that plays animation"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.play_img, _ = load_image("play.gif", -1)
        self.stop_img, _ = load_image("stop.gif", -1)
        self.set_is_playing(False)
    def set_is_playing(self, is_playing):
        if is_playing:
            self.image = self.stop_img
        else:
            self.image = self.play_img
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.bottom = rect.height - 10
        self.rect.centerx = rect.width // 2

def main():
    """Runs canvas code"""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption('Canvas')
    clock = pygame.time.Clock()

    # Prepare buttons
    play_stop_btn = PlayStopButton()
    next_btn = NextButton()
    prev_btn = PrevButton()

    # Prepare brush
    brush_size = 1
    brush_color = (0, 0, 0)
    brush = core.Brush(brush_size, brush_color)

    def add_new_frame():
        """Create new frame"""
        screen_size = screen.get_size()
        bgcolor = (255, 255, 255) # White
        animation.add_frame(core.Frame(*screen_size, bgcolor))

    # Prepare animation
    animation = core.Animation()
    add_new_frame()

    # Prepare font
    if pygame.font:
        font = pygame.font.Font(None, 36)

    def new_frame_text(current_frame, frame_cnt):
        """Create new Surface with current frame text rendered"""
        txt = f"{current_frame}/{frame_cnt}"
        frame_surf = font.render(txt, 1, (10, 10, 10))
        frame_rect = frame_surf.get_rect(left=10, top=10)
        return frame_surf, frame_rect

    # Prepare frame text
    if pygame.font:
        frame_surf, frame_rect = new_frame_text(1, 1)
    else:
        frame_surf = None

    # Group sprites
    allsprites = pygame.sprite.RenderPlain((play_stop_btn, next_btn, prev_btn))

    # State
    drawing = False
    playing = False

    # Main loop
    going = True
    while going:

        frame = animation.get_current_frame()
        img = frame.get_image()

        # Handle Input Events
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if play_stop_btn.rect.collidepoint(pos):
                    playing = not playing
                    if playing:
                        allsprites.remove(next_btn, prev_btn)
                        drawing = False
                    else:
                        allsprites.add(next_btn, prev_btn)
                    play_stop_btn.set_is_playing(playing)
                else:
                    if not playing:
                        if next_btn.rect.collidepoint(pos):
                            if animation.get_current_frame_index() == animation.get_frame_count() - 1:
                                add_new_frame()
                            animation.next_frame()
                        elif prev_btn.rect.collidepoint(pos):
                            animation.prev_frame()
                        else:
                            drawing = True
                            brush.press(*pos)
            elif event.type == MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    brush.move(img, *pos)

        if drawing:
            brush.move(img, *pos)

        animation.update()
        allsprites.update()
        animation.draw(screen)
        allsprites.draw(screen)

        if frame_surf:
            screen.blit(frame_surf, frame_rect)
            current_frame = animation.get_current_frame_index() + 1
            frame_cnt = animation.get_frame_count()
            frame_surf, frame_rect = new_frame_text(current_frame, frame_cnt)

        pygame.display.flip()

        if playing:
            animation.next_frame()
            clock.tick(animation.get_fps())

if __name__ == '__main__':
    main()
