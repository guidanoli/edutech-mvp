import os

import pygame
from pygame.locals import *

import jsonpickle

from tkinter import filedialog, Tk

from pathlib import Path

import core

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, '..', 'data')

def save_animation(animation):
    """Save animation"""
    root = Tk()
    root.withdraw()

    root.directory =  filedialog.askdirectory( \
        initialdir=Path.home(),
        title="Salvar projeto",
        mustexist=True)

    if not root.directory:
        return False

    animation.serialize(root.directory)

def load_animation():
    """Load animation"""
    root = Tk()
    root.withdraw()

    root.directory =  filedialog.askdirectory( \
        initialdir=Path.home(),
        title="Abrir projeto",
        mustexist=True)

    if not root.directory:
        return False

    return core.Animation.deserialize(root.directory)

def load_image(name, colorkey=None):
    """Loads image and returns image and its rectangle"""
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        raise SystemExit(f"Cannot load image: {fullname}") from err
    if name[-4:].lower() == '.png':
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class HelpScreen(pygame.sprite.Sprite):
    """Help screen"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.original, _ = load_image("controls.png", -1)
        self.image = self.rect = None
        self.reset_animation()

    def reset_animation(self):
        """Resets animation"""
        self.area_percentage = 0

    def update(self):
        """Overrides pygame.sprite.Sprite"""
        if self.area_percentage < 100:
            self.area_percentage += 1
            orig_rect = self.original.get_rect()
            size = [int(dim * self.area_percentage / 100) \
                for dim in orig_rect.size]
            self.image = pygame.transform.scale(self.original, size)
            angle = int(2 * 360 * self.area_percentage / 100)
            self.image = pygame.transform.rotate(self.image, angle)
            self.rect = self.image.get_rect()
            screen = pygame.display.get_surface()
            rect = screen.get_rect()
            self.rect.centerx = rect.centerx
            self.rect.centery = rect.centery - 50

class HelpButton(pygame.sprite.Sprite):
    """Button to get help"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("help.png", -1)
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.top = 8
        self.rect.right = rect.width - 40

class NextButton(pygame.sprite.Sprite):
    """Button to go to the next frame"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("next.gif", -1)
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.bottom = rect.height - 10
        self.rect.right = rect.width - 10

class PrevButton(pygame.sprite.Sprite):
    """Button to go to the previous frame"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image("prev.gif", -1)
        screen = pygame.display.get_surface()
        rect = screen.get_rect()
        self.rect.bottom = rect.height - 10
        self.rect.left = 10

class PlayStopButton(pygame.sprite.Sprite):
    """Button to play/stop animation"""
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
        self.rect.centerx = rect.centerx

def main():
    """Runs canvas code"""
    if not pygame.font:
        print('Warning, fonts disabled')

    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption('Canvas')
    clock = pygame.time.Clock()

    # Prepare screens
    help_screen = HelpScreen()

    # Prepare buttons
    play_stop_btn = PlayStopButton()
    next_btn = NextButton()
    prev_btn = PrevButton()
    help_btn = HelpButton()

    # Prepare palette
    palette = core.Palette()

    # Prepare brush
    brush_min_size = 1
    brush_max_size = 10
    brush_color = (0, 0, 0)
    brush = core.Brush(2, brush_color)

    def add_new_frame():
        """Create new frame"""
        screen_size = screen.get_size()
        bgcolor = (255, 255, 255) # White
        animation.add_frame(core.Frame(*screen_size, bgcolor))

    # Prepare animation
    min_fps = 1
    max_fps = 30
    animation = core.Animation(min_fps)
    add_new_frame()

    # Prepare font
    if pygame.font:
        font = pygame.font.Font(None, 36)

    def new_frame_text(current_frame, frame_cnt):
        """Create new Surface with current frame text rendered"""
        txt = f"Frame {current_frame} de {frame_cnt}"
        frame_surf = font.render(txt, 1, (10, 10, 10))
        frame_rect = frame_surf.get_rect(left=10, top=10)
        return frame_surf, frame_rect

    # Prepare frame text
    if pygame.font:
        frame_surf, frame_rect = new_frame_text(1, 1)
    else:
        frame_surf = None

    # Group sprites
    allsprites = pygame.sprite.RenderPlain( \
        (play_stop_btn, next_btn, prev_btn, help_btn))

    # State
    drawing = False
    playing = False
    helping = False
    color_history = [palette.get_current_color_name()]

    # Main loop
    going = True
    while going:
        
        # Get current frame and image
        frame = animation.get_current_frame()
        img = frame.get_image()

        # Handle Input Events
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    going = False
                elif event.key == K_g:
                    brush_size = brush.get_size()
                    if brush_size < brush_max_size:
                        brush.set_size(brush_size + 1)
                elif event.key == K_f:
                    brush_size = brush.get_size()
                    if brush_size > brush_min_size:
                        brush.set_size(brush_size - 1)
                elif event.key == K_r:
                    fps = animation.get_fps()
                    if fps < max_fps:
                        animation.set_fps(fps + 1)
                elif event.key == K_d:
                    fps = animation.get_fps()
                    if fps > min_fps:
                        animation.set_fps(fps - 1)
                elif event.key == K_u:
                    if len(color_history) > 1:
                        palette.set_current_color_by_name(color_history[-2])
                        color_history.append(color_history.pop(-2))
                        new_color = palette.get_color_dict()[color_history[-1]]
                        brush.set_color(new_color)
                elif event.key == K_a:
                    frame.clean()
                elif event.key == K_e:
                    if animation.get_frame_count() > 1:
                        frame_idx = animation.get_current_frame_index()
                        animation.remove_frame_at(frame_idx)
                elif event.key == K_s:
                    save_animation(animation)
                elif event.key == K_o:
                    tmp_animation = load_animation()
                    if tmp_animation:
                        animation = tmp_animation
            elif event.type == MOUSEBUTTONDOWN:
                if helping:
                    helping = False
                    allsprites.remove(help_screen)
                    continue
                if play_stop_btn.rect.collidepoint(pos):
                    playing = not playing
                    btns_to_hide = (next_btn, prev_btn, help_btn)
                    if playing:
                        allsprites.remove(*btns_to_hide)
                        drawing = False
                    else:
                        allsprites.add(*btns_to_hide)
                    play_stop_btn.set_is_playing(playing)
                else:
                    if playing:
                        continue
                    if next_btn.rect.collidepoint(pos):
                        if animation.get_current_frame_index() == \
                                animation.get_frame_count() - 1:
                            add_new_frame()
                        animation.next_frame()
                    elif prev_btn.rect.collidepoint(pos):
                        animation.prev_frame()
                    elif palette.rect.collidepoint(pos):
                        palette.next_color()
                        brush_color = palette.get_current_color()
                        brush.set_color(brush_color)
                    elif help_btn.rect.collidepoint(pos):
                        helping = True
                        help_screen.reset_animation()
                        allsprites.add(help_screen)
                    else:
                        drawing = True
                        current_color = palette.get_current_color_name()
                        if current_color != color_history[-1]:
                            color_history = color_history[-1:] + [current_color]
                        brush.press(*pos)
            elif event.type == MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    brush.move(img, *pos)
            elif event.type == MOUSEMOTION:
                if drawing:
                    brush.move(img, *pos)

        # Update animation and sprites
        animation.update()
        allsprites.update()

        # Draw animation
        animation.draw(screen)

        # Draw additional sprites
        allsprites.draw(screen)

        if not playing:
            palette.draw(screen)

        # Draw current frame
        if frame_surf:
            screen.blit(frame_surf, frame_rect)
            current_frame = animation.get_current_frame_index() + 1
            frame_cnt = animation.get_frame_count()
            frame_surf, frame_rect = new_frame_text(current_frame, frame_cnt)

        # Flip buffers
        pygame.display.flip()

        # Manage animation
        if playing:
            animation.next_frame()
            clock.tick(animation.get_fps())

if __name__ == '__main__':
    main()
