import pygame
import sys
from data.scripts.player import Player
from data.maps.levels import level1
from data.scripts.cameragroup import CameraGroup
from data.scripts.tilehandler import TileGroup
from data.scripts.tile import Tile

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

screen = pygame.display.set_mode((800, 450), 0, 32)
WIDTH, HEIGHT = screen.get_size()

display = pygame.Surface((WIDTH // 4, HEIGHT // 4))

playerSpriteSheet = pygame.image.load("data/images/player.png").convert()

player = Player(playerSpriteSheet, display.get_width() // 2, display.get_height() // 2)
tileHandler = TileGroup()

camera_group = CameraGroup(display)  # Use the screen dimensions
camera_group.add(player)  # Add the player and other sprites to the camera group


clock = pygame.time.Clock()
TILESIZE = 16
currentLevel = level1

y = 0
for row in currentLevel:
    x = 0
    for tile in row:

        if tile == 1:
            piece = Tile(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            tileHandler.add(piece)

        x += 1
    y += 1
camera_group.add_tile_group(tileHandler)

while True:
    display.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

    tileRects = tileHandler.get_rects()

    player.handle_states()
    player.handle_animation()
    player.move(tileRects)  # Move based on current state
    player.update()  # Update any final state changes (e.g., animations)
    camera_group.custom_draw(player)

    screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
    pygame.display.update()
    clock.tick(120)
