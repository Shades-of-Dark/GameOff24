import pygame


def lerp(start, end, factor):
    return start + (end - start) * factor


def smooth_step(edge0, edge1, x):
    # Scale and clamp x to the range [0, 1]
    x = max(0, min(1, (x - edge0) / (edge1 - edge0)))
    # Compute the smoothstep interpolation
    return x * x * (3 - 2 * x)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, display, dampening=0.15, zoom=1):
        super().__init__()
        self.offset = pygame.Vector2(0, 0)
        self.display = display
        self.dampening = dampening
        self.target_offset = pygame.Vector2(0, 0)
        self.zoom = zoom

    def apply_dampening(self, player):
        # Calculate target position
        target_x = player.rect.centerx - (self.display.get_width() // 2 / self.zoom)
        target_y = player.rect.centery - (self.display.get_height() // 2 / self.zoom)
        self.target_offset = pygame.Vector2(target_x, target_y)

        # Use smooth step for offset adjustment
        t = (self.offset - self.target_offset).length() / (self.display.get_width() // 2)  # Normalized distance
        t = smooth_step(0, 1, t)

        self.offset.x += (self.target_offset.x - self.offset.x) * t
        self.offset.y += (self.target_offset.y - self.offset.y) * t

    def custom_draw(self, player):
        # Calculate the offset based on the player's position
        self.apply_dampening(player)

        # Draw all sprites in the group with the camera offset
        for sprite in self:
            # Adjust the sprite position based on the camera offset for drawing only
            adjusted_position = (sprite.rect.topleft - self.offset) * self.zoom
            scaled_image = pygame.transform.scale(sprite.image, (
            int(sprite.rect.width * self.zoom), int(sprite.rect.height * self.zoom)))

            self.display.blit(scaled_image, (int(adjusted_position[0]), int(adjusted_position[1])))

            # Draw debugging rectangles at the adjusted position

    def add_tile_group(self, tile_group):
        # Add the entire tile group to the camera group
        self.add(tile_group)
