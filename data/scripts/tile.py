import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height, tiletype,
                 ramp=0):  # ramp = 0 is a normal tile # 1 = right 2 = left
        super().__init__()
        self.image = image
        self.ramp = ramp
        self.rect = pygame.FRect(x, y, width, height)
        self.tile = tiletype

    def draw(self, surface):
        # Draw the tile on the given surface
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (0, 255, 0), self.rect)


