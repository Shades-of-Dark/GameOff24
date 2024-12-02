import pygame


class Vector2(pygame.math.Vector2):
    pass


class Grass(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tiletype):
        super().__init__()
        self.ogimage = image

        self.rect = image.get_rect(center=(x, y))
        self.tile = tiletype
        self.angle = 0
        self.image = pygame.transform.rotate(self.ogimage, self.angle)
        self.startAngle = 0
        self.pos = Vector2(x, y)
        if self.tile == 13 or self.tile == 15:
            self.startAngle = 30
        elif self.tile == 14 or self.tile == 16:
            self.startAngle = -30

        self._layer = 5
        self.parallaxLayer = 2

    def bend_grass(self, player, wind):

        if player.rect.collidepoint(self.rect.center):  # if the player is touching the blade of grass
            if player.movement[0] >= 0:  # if they are moving right
                self.angle = abs(player.rect.centerx - self.rect.centerx) * -1.2  # bends the grass clockwise

            elif player.movement[0] <= 0:  # if they are moving left
                self.angle = abs(player.rect.centerx - self.rect.centerx) * 1.2  # bends the grass counterclockwise

        else:  # if not touching grass
            if wind == 0:  # if there is no wind
                # moves grass back to null (0) degrees
                if self.angle > self.startAngle:
                    self.angle -= 1
                elif self.startAngle > self.angle:
                    self.angle += 1

            else:
                # otherwise it sets the grass to the wind value
                self.angle = wind

        self.image = pygame.transform.rotate(self.ogimage, self.angle)

    def update(self, player, wind):

        if -30 < self.pos.x <= 240:

            self.bend_grass(player, wind)
