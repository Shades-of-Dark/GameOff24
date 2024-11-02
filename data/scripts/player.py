import pygame
import time


def get_image(surface, frame, width, height, color):
    handle_surf = surface.copy()
    clipRect = pygame.Rect(frame * width, 0, width, height)
    handle_surf.set_clip(clipRect)
    image = surface.subsurface(handle_surf.get_clip())
    image.set_colorkey(color)
    return image.copy()


class Vector2(pygame.Vector2):
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self, surf, x, y):
        super(Player, self).__init__()
        # ANIMATION STUFF
        NUMFRAMES = 9
        self.idleAnimation = [get_image(surf, i, surf.get_width() / NUMFRAMES, surf.get_height(), (255, 255, 255)) for i
                              in
                              range(3)]
        self.moveAnimation = [self.idleAnimation[0], ] + [
            get_image(surf, j, surf.get_width() / NUMFRAMES, surf.get_height(), (255, 255, 255)) for j in range(3, 6)]
        self.jumpAnimation = [get_image(surf, k, surf.get_width() / NUMFRAMES, surf.get_height(), (255, 255, 255)) for k
                              in range(6, 9)]
        self.currentAnimation = self.idleAnimation
        self.index = 0
        self.indexSpeed = 0.03
        self.image = self.idleAnimation[0]

        # STATES
        self.state = "idle"

        # PHYSICS STUFF
        self.pos = Vector2(x, y)
        self.rect = self.idleAnimation[0].get_frect(center=(self.pos.x, self.pos.y))
        self.movement = Vector2(0, 0)

        self.velocity = 3
        self.lastTime = time.time()
        self.dt = time.time() - self.lastTime
        self.dt *= 60
        self.lastTime = time.time()
        self.jumpCount = 10
        self.isJump = False
        self.GRAVITY = 0.8

    def move_left(self):
        self.movement.x -= self.velocity * self.dt

    def move_right(self):
        self.movement.x += self.velocity * self.dt

    def gravity(self):
        self.movement.y += self.GRAVITY

    def jump(self):
        self.movement.y -= self.jumpCount * abs(self.jumpCount) * 0.1
        self.jumpCount -= 1
        if self.jumpCount < -5:
            self.isJump = False

            self.jumpCount = 10

    def update(self):
        self.movement = Vector2(0, 0)
        self.dt = time.time() - self.lastTime
        self.dt *= 60
        self.lastTime = time.time()

        if self.isJump:
            self.jump()

        self.gravity()
        self.pos.y += self.movement.y
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

    def handle_animation(self):

        if self.state == "idle":
            self.currentAnimation = self.idleAnimation
            self.indexSpeed = 0.03

        elif self.state == "run":
            self.currentAnimation = self.moveAnimation
            self.indexSpeed = 0.13
        elif self.state == "fall":
            self.currentAnimation = self.jumpAnimation
            self.indexSpeed = 0.35
        elif self.state == "jump":
            self.currentAnimation = self.jumpAnimation
            self.indexSpeed = 0.3

        self.index += self.indexSpeed
        if self.index >= len(self.currentAnimation):
            self.index = 0

        self.image = self.currentAnimation[int(self.index)]

    def handle_states(self):
        if self.movement.x != 0:
            self.state = "run"
        elif self.movement.y < 0:
            self.state = "jump"
        elif self.movement.y > 0:
            self.state = "fall"
        else:
            self.state = "idle"

    def draw(self, surf):
        surf.blit(self.image, self.rect)
