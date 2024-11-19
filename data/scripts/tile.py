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


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, tiletype,
                 ramp=0):  # ramp = 0 is a normal tile # 1 = right 2 = left
        super().__init__()

        self.image = image
        self.ramp = ramp
        self.rect = pygame.FRect(x, y, width, height)
        self.tile = tiletype
        self.pos = Vector2(x, y)
        self.pulse_time = 0
        if self.tile != 12 and self.tile != 11:

            self.image.set_colorkey((255, 255, 255))
        else:
            self.ogimage = image
            self.image = self.ogimage.copy()

            self.transparentimg = palette_swap(self.image, (94, 80, 107), (137, 137, 137))  # (137, 137, 137))

    def handle_ghost_vision(self, display):
        pulseSpeed = 0.005
        if self.tile == 12 or self.tile == 11:
            self.pulse_time += pulseSpeed
            stuff = math.sin(self.pulse_time)
            pulse_amplitude = 0.1
            outer_radius = self.rect.width * (1 + stuff * pulse_amplitude)
            inner_radius = self.rect.width * 0.5 * (1 + stuff * pulse_amplitude)

            self.outerglow = circle_surf(outer_radius, (90, 70, 120))
            self.innerglow = circle_surf(inner_radius, (100, 80, 130))

            display.blit(self.outerglow, (self.pos.x - self.outerglow.get_width()/5, self.pos.y - self.outerglow.get_height()/4),
                         special_flags=pygame.BLEND_RGB_ADD)  # glow
            display.blit(self.innerglow, (self.pos.x, self.pos.y), special_flags=pygame.BLEND_RGB_ADD)

            self.image = self.ogimage

    def no_ghost_vision(self):
        if 12 == self.tile or self.tile == 11:
            self.image = self.transparentimg

    #        print("this should be invisible")
    #   print(self.transparentimg.get_colorkey())
