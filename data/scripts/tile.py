import pygame
import math

def circle_surf(radius, color, alpha=100):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, (*color, alpha), (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_c)

    surf.set_colorkey(old_c)

    img_copy.blit(surf, (0, 0))
    return img_copy.copy()


class Vector2(pygame.math.Vector2):
    pass


def get_pulse_alpha(time, min_alpha=128, max_alpha=255):
    # Adjust time to control the speed of pulsing
    pulse = (math.sin(time * 0.05) + 1) / 2  # Sine wave oscillation between 0 and 1
    return int(min_alpha + (max_alpha - min_alpha) * pulse)

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, tiletype,
                 ramp=0):  # ramp = 0 is a normal tile # 1 = right 2 = left
        super().__init__()

        self.image = image
        self.ramp = ramp
        self.rect = pygame.FRect(x, y, width, height)
        self.tile = tiletype
        self.pos = Vector2(x, y)

        if self.tile != 12 and self.tile != 11:

            self.image.set_colorkey((255, 255, 255))
        else:
            self.ogimage = image
            self.image = self.ogimage.copy()

            self.transparentimg = palette_swap(self.image, (94, 80, 107), (137, 137, 137))  # (137, 137, 137))
            self.outerglow = circle_surf(self.rect.width * 0, (90, 70, 120))
            self.innerglow = circle_surf(self.rect.width * 0.6, (100, 80, 130))

    def handle_ghost_vision(self, display):

        if self.tile == 12 or self.tile == 11:
            self.image = self.ogimage
            self.outerglow.set_alpha(get_pulse_alpha(pygame.time.get_ticks()))
            display.blit(self.outerglow, (self.pos.x - self.rect.width * 0.6, self.pos.y - self.rect.height * 0.6), special_flags=pygame.BLEND_RGB_ADD) #glow
            display.blit(self.innerglow, (self.pos.x - self.rect.width * 0.3, self.pos.y - self.rect.height * 0.3), special_flags=pygame.BLEND_RGB_ADD)

    def no_ghost_vision(self):
        if 12 == self.tile or self.tile == 11:
            self.image = self.transparentimg

    #        print("this should be invisible")
    #   print(self.transparentimg.get_colorkey())
