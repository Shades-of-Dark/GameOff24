import pygame


class TileGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_rects(self):
        tilerects = []
        for tile in self:
            tilerects.append(tile.rect)
        return tilerects
