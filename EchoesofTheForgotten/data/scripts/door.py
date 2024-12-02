import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, image, loc):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=loc)
        self._layer = 3
        self.parallaxLayer = 2
        self.pos = pygame.math.Vector2(loc[0], loc[1])

    def update(self, player):
        if self.rect.colliderect(player.rect):
            pass
