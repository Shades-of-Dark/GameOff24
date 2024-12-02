import pygame

pygame.init()


def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


def colour_swap(surf, old_c, new_c):
    img_copy = surf.copy()
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy


# method 3
def perfect_outline_2(surf, img, loc, outline_color):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()

    mask_surf = pygame.Surface(img.get_size())
    for pixel in mask_outline:
        mask_surf.set_at(pixel, outline_color)

    mask_surf.set_colorkey((0, 0, 0))
    surf.blit(mask_surf, (loc[0] - 1, loc[1]))
    surf.blit(mask_surf, (loc[0] + 1, loc[1]))
    surf.blit(mask_surf, (loc[0], loc[1] - 1))
    surf.blit(mask_surf, (loc[0], loc[1] + 1))


class Text(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.spacing = 1
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2', '3', '4',
                                '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']',
                                '*', '"', '<', '>', ';']
        font_img = pygame.image.load(path).convert()
        current_char_width = 0

        self._layer = 8
        self.parallaxLayer = 2
        self.characters = {}
        character_count = 0
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # Empty to start
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(0, 0)

        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height() + 1)
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1

        # Placeholder for the rendered text surface and rect

    def render(self, text, color, loc, scalefactor, outlinecolor, outline=True):
        """Render the text onto the sprite's surface."""
        x_offset = 0
        y_offset = 0
        text_width, text_height = 0, 8
        char_surfaces = []

        for char in text:
            if char not in [' ', '\r']:
                text_surf = self.characters[char]
                scaled_char = pygame.transform.scale(text_surf, (
                    text_surf.get_width() * scalefactor, text_surf.get_height() * scalefactor))

                new_char = colour_swap(scaled_char, (255, 0, 0), color)

                new_char.set_colorkey((0, 0, 0))

                char_surfaces.append((new_char, (x_offset, y_offset)))

                x_offset += scaled_char.get_width() + self.spacing
                text_width += scaled_char.get_width() + self.spacing

            elif char == '\r':
                y_offset += 8 * scalefactor
                text_height += 8 * scalefactor
                x_offset = 0
            else:
                x_offset += text_surf.get_width() * scalefactor + self.spacing
                text_width += text_surf.get_width() * scalefactor + self.spacing

        # Create the image for the text
        self.image = pygame.Surface((text_width, text_height), pygame.SRCALPHA)

        for char_surf, pos in char_surfaces:

            if outline:
                perfect_outline_2(self.image, char_surf, pos, outlinecolor)
            self.image.blit(char_surf, pos)

        self.rect = self.image.get_rect(topleft=loc)
