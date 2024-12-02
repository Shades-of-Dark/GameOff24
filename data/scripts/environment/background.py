import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, image, x, y, layer, parallaxLayer, color):
        super().__init__()
        self._layer = layer
        self.parallaxLayer = parallaxLayer
        self.image = image
        self.image.set_colorkey(color)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)
        self.x, self.y = x,y
        self.rect.x, self.rect.y = x,y



