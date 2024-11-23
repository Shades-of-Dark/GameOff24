import pygame
import random


class Stalactite(pygame.sprite.Sprite):
    def __init__(self, color, width, height, points, loc):
        super(Stalactite, self).__init__()
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.set_colorkey((0, 0, 0))
        self.points = points

        pygame.draw.polygon(self.image, self.color, points)
        self.rect = self.image.get_rect(center=loc)

        self.loc = loc
        self.pos = pygame.math.Vector2(loc[0], loc[1])
        self._layer = 1
        self.parallaxLayer = 0

    def update_cavern_wall(self, display, player):
        self.display = display

        last_x, last_y = self.points[-1]

        # Generate points ahead of the player
        while self.loc[0] + last_x < player.rect.centerx:
            new_x = last_x + random.randint(50, 150)  # Distance to next point
            new_y = last_y + random.randint(-self.image.get_height()//4, int(self.image.get_height() * 3/4 + 0.5))  # Variation in height

            self.points.append((new_x, new_y))
            last_x, last_y = new_x, new_y

        # Optionally, remove points far behind the player to optimize performance

        self.image.fill((0,0,0))
        pygame.draw.polygon(self.image, self.color, self.points)
        self.image.set_colorkey((0,0,0))
        print(len(self.points))
