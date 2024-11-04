import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = image

        self.rect = pygame.FRect(x, y, width, height)

    def draw(self, surface):
        # Draw the tile on the given surface
        pygame.draw.rect(surface, (255, 255, 255), self.rect)  # Example color
