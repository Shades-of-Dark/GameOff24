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
        self.vertical_velocity = 0
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
        self.direction = True  # TRUE MEANING LEFT FALSE MEANING RIGHT
        self.left = False
        self.right = False
        # PHYSICS STUFF
        self.pos = Vector2(x, y)
        self.rect = self.idleAnimation[0].get_frect(center=(self.pos.x, self.pos.y))
        self.movement = Vector2(0, 0)

        self.maxVelocity = 1.2
        self.speed = float(0)
        self.acceleration = float(self.maxVelocity / 6)  # amount of frames till the character reaches max speed
        self.deceleration = float(self.maxVelocity / 3)

        self.lastTime = time.time()
        self.dt = time.time() - self.lastTime
        self.dt *= 60
        self.lastTime = time.time()

        self.jump_timer = 0
        self.max_jump_duration = 20
        self.jumpGravity = 0.5
        self.isJump = False

        self.coyoteTime = 0.9

        self.GRAVITY = 0.8
        self.onGround = False

        self.ghostEnergy = 0
        self.energyConsumption = 1
        self.ghostVision = False

    def move_left(self):
        self.movement.x -= self.speed * self.dt

        if self.speed <= self.maxVelocity:
            self.speed += self.acceleration * self.dt
        self.direction = True

    def move_right(self):
        self.movement.x += self.speed * self.dt
        if self.speed <= self.maxVelocity:
            self.speed += self.acceleration * self.dt
        self.direction = False

    def handle_jump(self):
        if self.isJump:
            self.vertical_velocity += self.jumpGravity * self.dt
            self.movement[1] += self.vertical_velocity * self.dt
            self.vertical_velocity -= 0.1 * self.vertical_velocity

            if self.vertical_velocity < 0:  # Going up

                self.jumpGravity = 0.3  # Lower gravity
            else:  # Falling down
                self.jumpGravity = 0.45  # Normal gravity

            self.jump_timer += 1 * self.dt

            if self.jump_timer > self.max_jump_duration:
                self.jump_timer = 0
                self.isJump = False

    def friction(self):
        if self.state == "idle":
            # Calculate frame-rate-adjusted deceleration
            if not self.left and not self.right:
                frame_deceleration = self.deceleration * self.dt

                # Apply friction in the opposite direction of movement
                if self.direction:  # Assuming direction True is right
                    self.movement[0] -= frame_deceleration
                else:  # direction False is left
                    self.movement[0] += frame_deceleration

                # Zero out small speeds to avoid flickering
                if round(abs(self.movement[0]), 2) < 0.44:  # Threshold to consider speed "stopped"
                    self.movement[0] = 0
                    self.speed = 0  # Fully stop if below the threshold

                # Update speed to reflect absolute movement
                self.speed = abs(self.movement[0])

    def gravity(self):
        self.movement.y += self.GRAVITY * self.dt

    def delta_time_update(self):
        self.dt = time.time() - self.lastTime
        self.dt *= 60
        self.lastTime = time.time()

    def jump(self):
        if self.coyoteTime > 0:
            self.vertical_velocity = -9  # Adjust for jump height
            self.isJump = True
            self.jump_timer = 0
            self.onGround = False

    def update(self):
        self.movement = Vector2(0, 0)
        self.delta_time_update()

        if self.onGround:
            self.coyoteTime = 0.9
        else:
            if self.coyoteTime > 0:
                self.coyoteTime -= 0.1

        self.handle_jump()

        if self.left:
            self.move_left()
        elif self.right:
            self.move_right()

        self.friction()
        self.gravity()
        self.use_ghost_vision()

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
            self.indexSpeed = 0.2

        self.index += self.indexSpeed * self.dt
        if self.index >= len(self.currentAnimation):
            self.index = 0

        self.image = pygame.transform.flip(self.currentAnimation[int(self.index)], self.direction, False)

    def handle_states(self):
        if self.movement.x != 0 and self.onGround:
            self.state = "run"
        elif self.movement.y < 0:
            self.state = "jump"
        elif self.movement.y > 0 and not self.onGround:
            self.state = "fall"
        else:
            self.state = "idle"

    def hit_list(self, tiles):
        collisions = []
        for tile in tiles:
            if tile.colliderect(self.rect):
                collisions.append(tile)
        return collisions

    def move(self, tiles):
        self.onGround = False
        self.pos.x += self.movement.x
        self.rect.x = self.pos.x

        x_collisions = self.hit_list(tiles)

        for tile in x_collisions:
            if self.movement.x > 0:
                self.rect.right = tile.left
            elif self.movement.x < 0:
                self.rect.left = tile.right
        self.pos.x = self.rect.x

        self.pos.y += self.movement.y
        self.rect.y = self.pos.y
        y_collisions = self.hit_list(tiles)

        for tile in y_collisions:
            if self.movement.y > 0:
                self.rect.bottom = tile.top
                self.onGround = True
            elif self.movement.y < 0:
                self.rect.top = tile.bottom

        self.pos.y = self.rect.y

    def use_ghost_vision(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            if self.ghostEnergy > 0:
                self.ghostVision = True
                self.ghostEnergy -= self.energyConsumption
