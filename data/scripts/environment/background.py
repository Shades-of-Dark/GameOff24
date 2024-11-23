import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self._layer = 0
        self.parallaxLayer = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)
        self.x, self.y = x,y
        self.rect.x, self.rect.y = x,y

    def update(self, player, display):
        for x in range(5):

            display.blit(self.image, (self.x + self.image.get_width() * x + self.pos.x, self.y+ self.pos.y))

