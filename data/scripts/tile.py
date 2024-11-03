import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = pygame.FRect(x, y, width, height)

    def draw(self, surface):
        # Draw the tile on the given surface
        pygame.draw.rect(surface, (255, 255, 255), self.rect)  # Example color
