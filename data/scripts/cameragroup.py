import pygame
import random


def lerp(start, end, factor):
    return start + (end - start) * factor


def smooth_step(edge0, edge1, x):
    # Scale and clamp x to the range [0, 1]
    x = max(0, min(1, (x - edge0) / (edge1 - edge0)))
    # Compute the smoothstep interpolation
    return x * x * (3 - 2 * x)


class CameraGroup(pygame.sprite.LayeredUpdates):
    def __init__(self, display, dampening=0.15, zoom=1):
        super().__init__()
        self.offset = pygame.Vector2(0, 0)
        self.display = display
        self.dampening = dampening
        self.target_offset = pygame.Vector2(0, 0)
        self.zoom = zoom

        # Camera shake variables
        self.shake_intensity = 0  # Shake intensity, controls how much the camera shakes
        self.shake_duration = 0  # Duration of the shake in frames
        self.max_shake_intensity = 10  # Maximum intensity of shake (pixels)
        self.shake_decay = 0.1  # Decay factor for the shake intensity

        self.parallax_layers = []
        self.speed_multipliers = {
            -1: 0.3,
            0: 0.5,  # Background moves slower
            1: 0.8,  # Midground moves normally
            2: 1.0  # Foreground moves faster
        }

    def generate_parallax_layer(self):
        """Add a parallax layer with a specific speed."""
        self.layers = {}
        for sprite in self:

            layer = sprite.parallaxLayer
            if layer not in self.layers:
                self.layers[layer] = pygame.sprite.Group()
            self.layers[layer].add(sprite) # associates sprite with a certain layers sprite group

        # Assign speed multipliers to each layer (you can customize this mapping)

        # Save the layers with their speeds
        for layer, sprites in sorted(self.layers.items()):  # Sort to ensure proper draw order

            speed = self.speed_multipliers.get(layer, 1.0)  # Default to normal speed
            self.parallax_layers.append([sprites, speed])

    def update_parallax(self):
        for sprite in self.sprites():
            if sprite not in self.parallax_layers:
                self.parallax_layers[sprite.parallaxLayer + 1][0].add(sprite)

    def apply_dampening(self, player):
        # Calculate target position
        target_x = player.rect.centerx - (self.display.get_width() // 2 / self.zoom)
        target_y = player.rect.centery - (self.display.get_height() // 2 / self.zoom)
        self.target_offset = pygame.Vector2(target_x, target_y)

        # Use smooth step for offset adjustment

        speed = (self.target_offset.x - self.offset.x) * player.dt

        self.offset.x += speed

        top_threshold = self.display.get_height() * 0.3
        bottom_threshold = self.display.get_height() * 0.7

        #   camera_box = pygame.Rect(0, top_threshold, self.display.get_width(),
        #          bottom_threshold - top_threshold)
        #   pygame.draw.rect(self.display, (255, 0, 0), camera_box, 3)         # trying to visualize bounds of camera

        self.offset.x = lerp(self.offset.x, self.target_offset.x, self.dampening)
        self.offset.y = lerp(self.offset.y, self.target_offset.y, self.dampening)

        if player.rect.top < top_threshold:
            self.offset.y += (self.target_offset.y - self.offset.y) * 0.1
        elif player.rect.bottom > bottom_threshold:
            self.offset.y += (self.target_offset.y - self.offset.y) * 0.1

            # Apply camera shake
        if self.shake_intensity > 0:
            shake_offset = pygame.Vector2(
                random.uniform(-self.shake_intensity, self.shake_intensity),
                random.uniform(-self.shake_intensity, self.shake_intensity)
            )
            self.offset += shake_offset
            self.shake_duration -= 1  # Decrease shake duration
            self.shake_intensity -= self.shake_decay  # Decay the intensity

            if self.shake_duration <= 0:
                self.shake_intensity = 0  # Reset shake if duration is over

    def start_shake(self, intensity, duration):
        """Start a camera shake with a given intensity and duration."""
        self.shake_intensity = intensity
        self.shake_duration = duration

    def draw_sprite(self, sprite, offset):
        # Adjust the sprite's position based on the given offset

        adjusted_position = (sprite.rect.topleft - offset) * self.zoom

        # Scale the sprite's image based on the current zoom
        scaled_image = pygame.transform.scale(
            sprite.image,
            (
                round(sprite.image.get_width() * self.zoom),
                round(sprite.image.get_height() * self.zoom)
            )
        )

        # Blit the scaled sprite image to the display
        sprite.pos.xy = (round(adjusted_position[0]), round(adjusted_position[1]))
        self.display.blit(scaled_image, sprite.pos.xy)

    def custom_draw(self, player):
        # Apply dampening to calculate the camera offset
        self.apply_dampening(player)

        # Draw parallax layers
        for layer_sprites, speed in self.parallax_layers:
            parallax_offset = self.offset * speed

            for sprite in layer_sprites:
                self.draw_sprite(sprite, parallax_offset)

    def add_tile_group(self, tile_group):
        # Add the entire tile group to the camera group
        self.add(tile_group)
