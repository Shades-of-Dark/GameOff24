import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, color, loc, size, displaysize:tuple, xvel, yvel):
        super().__init__()

        self.color = color
        self.image = pygame.Surface((size * 2, size * 2))
        self.rect = self.image.get_rect(topleft=loc)
        self.displaySize = displaysize
        self.size = size
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.image.set_colorkey((0, 0, 0))
        self._layer = 4
        self.parallaxLayer = 2
        self.pos = pygame.math.Vector2(loc[0], loc[1])
        self.xvel = xvel
        self.yvel = yvel

    def update(self):

        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, self.color, (int(self.size), int(self.size)), int(self.size))
        self.image.set_colorkey((0, 0, 0))

        self.size -= 0.1
        if self.size <= 0:
            self.kill()

        self.rect.x += self.xvel
        self.rect.y += self.yvel

        self.yvel += 0.2

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def bounce(self):
        self.yvel *= -1

