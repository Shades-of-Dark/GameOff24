import pygame


class Energy(pygame.sprite.Sprite):
    def __init__(self, image, loc):
        super().__init__()
        self.ogimage = image
        self.image = image
        self.rect = image.get_rect(center=(loc[0], loc[1]))
        self.angle = 0
        self.pos = pygame.math.Vector2(loc[0], loc[1])
        self.parallaxLayer =  3
        self._layer = 3

    def update(self, player, energylist, energysound):
        self.image = pygame.transform.rotate(self.ogimage, int(self.angle))
        self.angle += 1
        if player.rect.colliderect(self.rect):
            player.ghostEnergy += 80
            energysound.play()
            energylist.remove(self)
            self.kill()


