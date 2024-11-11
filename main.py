import math
import random
import pygame
import sys
from data.scripts.player import Player
from data.maps.levels import level1
from data.scripts.cameragroup import CameraGroup
from data.scripts.tilehandler import TileGroup
from data.scripts.tile import Tile
from data.scripts.grass import Grass

'''Concept: Echoes of the Forgotten
Core Idea:
You play as Lumi, a relic hunter in a lost underground city filled with enchanted doors, moving walls, and hidden paths that shift with every step.
Mechanic: Lumi has a “ghost vision” ability that reveals remnants of the city’s past—phantom-like glimpses of past citizens, doors, or passages visible only in ghost vision mode.
Lumi must switch between regular and ghost vision to uncover secret paths, solve environmental puzzles, and learn hidden details about the city.
Gameplay:
Primary Mechanic – Ghost Vision:

Players toggle into ghost vision to reveal secrets. Only in ghost vision can Lumi see hidden doors, platforms, and ancient messages from the city’s inhabitants.
Ghost vision uses up “energy,” which players need to manage. Lumi can recharge it by finding certain crystals or by completing puzzles, keeping gameplay balanced and challenging.
Secret Layers and Traps:

Some paths are only accessible in ghost vision, while others might disappear if ghost vision is used, creating a back-and-forth exploration between both views.
Hidden traps or dead ends could be visible in one view but not the other, encouraging players to switch frequently and stay alert.
Puzzle Integration:

Certain puzzles might require the player to memorize clues from ghost vision before switching back, like matching symbols or remembering pathways.
Each level could have a simple objective, like “find the three hidden relics,” each of which unlocks a part of the city’s lore.
Visual Style:

Use eerie, translucent sprites for ghost objects, characters, and walls in ghost vision. Flickering lights, subtle animations, and ghostly visual effects would add atmosphere.
The regular world could feel dark and abandoned, with the ghost vision revealing the city's lively past—giving players glimpses of bustling markets, former citizens, and ancient architecture in pixel art.
Optional Extras (If Time Allows):
Secret Notes or Runes: Hidden messages written on walls only visible in ghost vision that reveal lore bits about the city and add mystery.
Ghost NPCs: Occasionally, Lumi encounters a ghost NPC who reveals the city’s history or gives hints to find powerful relics.
Why It Works:
This approach uses a simple toggle mechanic to add depth and exploration.
It’s perfect for pixel art since ghostly figures, shadowy objects, and old cityscapes can be visually striking.
With both worlds, you have room for atmospheric, eerie pixel art details, giving players the feeling of unlocking an ancient, forgotten place full of secrets.
Let me know if this sparks any ideas or if you'd like help on specifics, like implementing ghost vision!'''

pygame.init()

screen = pygame.display.set_mode((960, 540), 0, 32)
WIDTH, HEIGHT = screen.get_size()

display = pygame.Surface((WIDTH//4, HEIGHT//4))

playerSpriteSheet = pygame.image.load("data/images/player.png").convert()

player = Player(playerSpriteSheet, display.get_width() // 2, display.get_height() // 2)
tileHandler = TileGroup()

camera_group = CameraGroup(display)  # Use the screen dimensions
camera_group.add(player)  # Add the player and other sprites to the camera group

pygame.display.set_caption("Echoes of the Forgotten")


def get_image(surface, frame, width, height, color, column, scale):
    handle_surf = surface.copy()
    clipRect = pygame.Rect(frame * width, column * height, width, height)
    handle_surf.set_clip(clipRect)
    image = surface.subsurface(handle_surf.get_clip())
    image.set_colorkey(color)
    image = pygame.transform.scale(image, (scale, scale))
    return image.copy()


clock = pygame.time.Clock()
TILESIZE = 16
currentLevel = level1

tileSpriteSheet = pygame.image.load("data/images/mocktileset.png").convert()

p = 0
tileDict = dict()
for row in range(4):
    for tile in range(4):
        p += 1
        tileImage = get_image(tileSpriteSheet, frame=tile, width=TILESIZE, height=TILESIZE, color=(255, 255, 255),
                              column=row, scale=TILESIZE)

        tileDict[p] = tileImage

grassSpriteSheet = pygame.image.load("data/images/grassblades.png").convert()
blades = []
weirdoblades = []
for blade in range(6):
    grassImg = get_image(grassSpriteSheet, blade, 8, 8, (0, 0, 0), 0, TILESIZE)
    if blade < 3:
        blades.append(grassImg)
    else:
        weirdoblades.append(grassImg)

grassGroup = pygame.sprite.Group()
numBladesPerTile = 8
y = 0
for row in currentLevel:
    x = 0
    for tile in row:
        ramp = 0
        if tile != 0:
            coords = (x * TILESIZE, y * TILESIZE)

            if tile == 13 or tile == 15:
                ramp = 1
                for i in range(random.randint(2, numBladesPerTile)):
                    goofy = random.randint(1, TILESIZE)
                    grassBlade = Grass(random.choice(blades), coords[0] + goofy, coords[1] + goofy, tile)
                    grassGroup.add(grassBlade)
            elif tile == 14 or tile == 16:
                ramp = 2
                for i in range(random.randint(2, numBladesPerTile)):
                    goofy = random.randint(1, TILESIZE)
                    grassBlade = Grass(random.choice(blades), coords[0] + goofy, coords[1] + goofy, tile)
                    grassGroup.add(grassBlade)

            elif tile in [1, 2, 3, 4, 7, 8]:
                for i in range(random.randint(2, numBladesPerTile)):
                    grassBlade = Grass(random.choice(blades), coords[0] + random.randint(0, TILESIZE), coords[1] - 2, tile)
                    grassGroup.add(grassBlade)

            elif tile == 11 or tile == 12:
                for i in range(random.randint(2, numBladesPerTile)):
                    grassBlade = Grass(random.choice(weirdoblades), coords[0] + random.randint(0, TILESIZE), coords[1] - 2, tile)
                    grassGroup.add(grassBlade)
            piece = Tile(tileDict[tile], coords[0], coords[1], TILESIZE, TILESIZE, tile, ramp)
            tileHandler.add(piece)

        x += 1
    y += 1

camera_group.add_tile_group(tileHandler)
camera_group.add(grassGroup)

visionoverlay = pygame.Surface(screen.get_size())
visionoverlay.fill((10, 60, 70))
visionoverlay.set_alpha(125, pygame.BLEND_RGBA_ADD)
wind = 0
windBend = 0
windEvent = pygame.USEREVENT + 1
pygame.time.set_timer(windEvent, 1500)

while True:
    display.fill((250, 250, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == windEvent:
            wind = random.randint(-1, 1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left = True

            if event.key == pygame.K_RIGHT:
                player.right = True

            if event.key == pygame.K_SPACE:  # For jumping
                player.jump()

        #  if event.type == pygame.MOUSEBUTTONDOWN:
        #    if event.button == 5:
        #      camera_group.zoom -= 0.02
        #   elif event.button == 4:
        #   camera_group.zoom += 0.02

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left = False
            if event.key == pygame.K_RIGHT:
                player.right = False

    if wind * 15 > windBend:
        windBend += 1
    elif wind * 15 < windBend:
        windBend -= 1
    grassGroup.update(player, windBend)

    player.handle_states()
    player.handle_animation()
    player.update()  # Update any final state changes (e.g., animations)
    player.move(tileHandler)
    camera_group.custom_draw(player)

    screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
    if player.ghostVision:
        screen.blit(visionoverlay, (0, 0))

    pygame.display.update()
    clock.tick(60)
