import random
import sys

import pygame
import math
from data.scripts.particle import Particle
from data.maps.levels import level1
from data.scripts.cameragroup import CameraGroup
from data.scripts.door import Door
from data.scripts.energy import Energy
from data.scripts.environment.background import Background
from data.scripts.grass import Grass
from data.scripts.pixelfont import Font
from data.scripts.player import Player
from data.scripts.tile import Tile
from data.scripts.tilehandler import TileGroup
from data.scripts.text import Text

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

display = pygame.Surface((WIDTH // 4, HEIGHT // 4))


def menu():
    def get_image(surface, frame, width, height, color, column, scale):
        handle_surf = surface.copy()
        clipRect = pygame.Rect(frame * width, column * height, width, height)
        handle_surf.set_clip(clipRect)
        image = surface.subsurface(handle_surf.get_clip())
        image.set_colorkey(color)
        image = pygame.transform.scale(image, (scale, scale))
        return image.copy()

    blipSound = pygame.mixer.Sound("data/sfx/blipSelect.wav")
    play = pygame.image.load("data/images/play.png").convert()
    normal = get_image(play, 0, color=(254, 255, 255), column=0, scale=32, width=32, height=16)
    clickednormal = get_image(play, 1, color=(254, 255, 255), column=0, scale=32, width=32, height=16)
    go = True
    buttonRect = pygame.Rect(display.get_width() // 2 - normal.get_width() // 2,
                             display.get_height() // 2 - normal.get_width() // 2, normal.get_width(),
                             normal.get_height())
    clock = pygame.time.Clock()
    pygame.display.set_caption("Echoes of the Forgotten")
    while go:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                blipSound.play()
                if buttonRect.collidepoint(mx // 4, my // 4):
                    go = False
                    game()

        if buttonRect.collidepoint(mx // 4, my // 4):
            display.blit(clickednormal, buttonRect)

        else:
            display.blit(normal, buttonRect)

        screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(60)


def game():
    playerSpriteSheet = pygame.image.load("data/images/player.png").convert()

    player = Player(playerSpriteSheet, display.get_width() // 2, display.get_height() // 2)
    tileHandler = TileGroup()

    camera_group = CameraGroup(display)  # Use the screen dimensions
    camera_group.add(player)  # Add the player and other sprites to the camera group

    pygame.display.set_caption("Echoes of the Forgotten")

    def circle_surf(radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def get_image(surface, frame, width, height, color, column, scale):
        handle_surf = surface.copy()
        clipRect = pygame.Rect(frame * width, column * height, width, height)
        handle_surf.set_clip(clipRect)
        image = surface.subsurface(handle_surf.get_clip())
        image.set_colorkey(color)
        image = pygame.transform.scale(image, (scale, scale))
        return image.copy()

    def get_image_for_pallete_swap(surface, frame, width, height, column,
                                   scale):  # same thing just doesnm't include the color for palette swapping
        handle_surf = surface.copy()
        clipRect = pygame.Rect(frame * width, column * height, width, height)
        handle_surf.set_clip(clipRect)
        image = surface.subsurface(handle_surf.get_clip())
        image = pygame.transform.scale(image, (scale, scale))
        return image.copy()

    clock = pygame.time.Clock()
    TILESIZE = 16
    currentLevel = level1

    tileSpriteSheet = pygame.image.load("data/images/mocktileset.png").convert()

    p = 0
    tileDict = dict()
    for row in range(6):
        for tile in range(4):
            p += 1
            tileImage = get_image_for_pallete_swap(tileSpriteSheet, frame=tile, width=TILESIZE, height=TILESIZE,
                                                   column=row, scale=TILESIZE)

            tileDict[p] = tileImage.convert()

    grassSpriteSheet = pygame.image.load("data/images/grassblades.png").convert()

    blades = []
    weirdoblades = []
    for blade in range(6):
        grassImg = get_image(grassSpriteSheet, blade, 8, 8, (0, 0, 0), 0, TILESIZE)
        if blade < 3:
            blades.append(grassImg.convert())
        else:
            weirdoblades.append(grassImg.convert())

    grassGroup = pygame.sprite.Group()
    numBladesPerTile = 8

    energyImage = pygame.image.load("data/images/energy.png").convert()
    energyImage.set_colorkey((0, 0, 0))
    energy = []
    y = 0

    doors = []
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
                        grassBlade = Grass(random.choice(blades), coords[0] + goofy // 2, coords[1] + goofy, tile)
                        grassGroup.add(grassBlade)
                elif tile == 14 or tile == 16:
                    ramp = 2
                    for i in range(random.randint(2, numBladesPerTile)):
                        goofy = random.randint(1, TILESIZE)
                        grassBlade = Grass(random.choice(blades), coords[0] + goofy, coords[1] + goofy, tile)
                        grassGroup.add(grassBlade)
                if tile == 25:
                    mana = Energy(energyImage, coords)
                    energy.append(mana)
                    camera_group.add(mana)
                else:

                    if tile == 23:
                        doors.append(Door(tileDict[23], coords))

                    piece = Tile(tileDict[tile], coords[0], coords[1], TILESIZE, TILESIZE, tile, ramp)
                    tileHandler.add(piece)

                if tile in [1, 2, 3, 4, 7, 8]:
                    for i in range(random.randint(2, numBladesPerTile)):
                        grassBlade = Grass(random.choice(blades), coords[0] + random.randint(0, TILESIZE),
                                           coords[1] - 2,
                                           tile)
                        grassGroup.add(grassBlade)
                    for i in range(random.randint(1, numBladesPerTile // 2)):
                        grassBlade = Grass(random.choice(weirdoblades), coords[0] + random.randint(0, TILESIZE),
                                           coords[1] - 2, tile)
                        grassGroup.add(grassBlade)

            x += 1
        y += 1

    background = pygame.image.load("data/images/background.png").convert()
    mountains = pygame.image.load("data/images/moutains.png").convert()
    cavernwall = pygame.image.load("data/images/cavernwall.png").convert()
    midground = pygame.image.load("data/images/midground.png").convert()

    backgroundextension = pygame.Surface((500, 500))
    backgroundextension.fill((16, 17, 34))

    for p in range(-3, 3):
        mountainsObj = Background(mountains, p * mountains.get_width(), 0, -1, -1, (0, 0, 0))
        camera_group.add(mountainsObj)

    for t in range(-3, 3):
        midgroundObj = Background(midground, t * midground.get_width(), 0, 1, 1, (255, 255, 255))
        camera_group.add(midgroundObj)

    for s in range(-3, 3):
        cavernwallLayer = Background(cavernwall, s * cavernwall.get_width(), 20, 2, 1, (0, 0, 0))

        camera_group.add(cavernwallLayer)

    for r in range(-3, 3):
        backgroundObjExtension = Background(backgroundextension, -200 + r * backgroundextension.get_width(), 125, 0, 0,
                                            (0, 0, 0))
        camera_group.add(backgroundObjExtension)

    for q in range(-3, 3):
        backgroundObj = Background(background, q * background.get_width(), 10, 0, 0, (0, 0, 0))
        camera_group.add(backgroundObj)

    camera_group.add_tile_group(tileHandler)
    camera_group.add(grassGroup)

    visionoverlay = pygame.Surface((screen.get_width() // 4, screen.get_height() // 4))
    visionoverlay.fill((30, 90, 100))
    visionoverlay.set_alpha(105)
    wind = 0
    windBend = 0
    windEvent = pygame.USEREVENT + 1
    weirdEvent = pygame.USEREVENT + 2
    pygame.time.set_timer(windEvent, 1500)
    pygame.time.set_timer(weirdEvent, 5000)
    scalesize = (240, 135)

    layers = {}
    for sprite in camera_group:
        layer = sprite.parallaxLayer
        if layer not in layers:
            layers[layer] = []
        layers[layer].append(sprite)

    textpath = "data/images/font.png"
    font = Font(textpath)
    cameraAdjustedText = Text(textpath)
    cameraAdjustedText.render(text="Press G to enter ghost vision", color=(255, 255, 255), loc=(120, 60),
                              scalefactor=1,
                              outlinecolor=(12, 230, 242))

    othertext = Text(textpath)
    othertext.render("You're gonna need ghost vision here...", color=(255, 255, 255), loc=(430, 170),
                     scalefactor=1,
                     outlinecolor=(12, 230, 242))
    camera_group.add(cameraAdjustedText)
    camera_group.add(othertext)
    game_time = 0
    somerot = 0
    music = pygame.mixer.Sound("data/music/lumi.wav")

    jump = pygame.mixer.Sound("data/sfx/jump.wav")
    powerUp = pygame.mixer.Sound("data/sfx/powerUp.wav")

    jump.set_volume(0.4)
    music.set_volume(0.4)
    powerUp.set_volume(0.4)
    music.play(-1)

    whisper = pygame.mixer.Sound("data/music/whispers.wav")
    whisper.set_volume(0.05)

    hurt = pygame.mixer.Sound("data/sfx/hitHurt.wav")

    particles = pygame.sprite.Group()

    camera_group.generate_parallax_layer()

    changeinlength = len(camera_group)

    run = True
    while run:
        display.fill((78, 106, 116))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == windEvent:
                wind = random.randint(-1, 1)
            if event.type == weirdEvent:
                whisper.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left = True

                if event.key == pygame.K_RIGHT:
                    player.right = True

                if event.key == pygame.K_UP:  # For jumping
                    player.jump(jump)

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

        player.handle_states(hurt)
        player.handle_animation()
        player.update()  # Update any final state changes (e.g., animations)
        player.move(tileHandler)

        # ____________________________DRAW AND UPDATE WINDOW__________________________________________________#
        for chi in energy[:]:
            chi.update(player, energy, powerUp)
        for door in doors[:]:
            door.update(player)

        camera_group.custom_draw(player)

        if changeinlength != len(camera_group):
            camera_group.update_parallax()
            changeinlength = len(camera_group)
        # background
        b_points = [[0, 16]]
        b_points += [[display.get_width() / 30 * (i + 1) + math.sin((game_time + i * 120) / 4) * 8,
                      16 + math.sin((game_time + i * 10) / 10) * 4] for i in range(29)]

        b_points += [[display.get_width(), 16], [display.get_width(), 0], [0, 0]]
        b2_points = [[0, 16]]
        b2_points += [[display.get_width() / 30 * (i + 1) + math.sin((game_time + i * 120) / 10) * 8,
                       16 + math.sin((game_time + i * 10) / 10) * 4] for i in range(29)]
        b2_points += [[display.get_width(), 16], [display.get_width(), 0], [0, 0]]
        b2_points = [[display.get_width() - p[0], p[1] * 2] for p in b2_points]
        back_surf = pygame.Surface((display.get_width(), 72))
        pygame.draw.polygon(back_surf, (15, 10, 24), b2_points)
        back_surf.set_colorkey((0, 0, 0))
        back_surf.set_alpha(200)
        display.blit(back_surf, (0, 0))
        display.blit(pygame.transform.flip(back_surf, False, True), (0, display.get_height() - 72))
        # background

        # border fog
        fog_surf = pygame.Surface((display.get_width(), 24))
        pygame.draw.polygon(fog_surf, (0, 2, 4), b_points)
        fog_surf.set_alpha(150)
        fog_surf.set_colorkey((0, 0, 0))
        display.blit(pygame.transform.flip(fog_surf, True, False), (0, -6))
        display.blit(fog_surf, (0, 0))
        display.blit(pygame.transform.flip(fog_surf, True, True), (0, display.get_height() - 24 + 6))
        display.blit(pygame.transform.flip(fog_surf, False, True), (0, display.get_height() - 24))
        side_fog = pygame.transform.scale(pygame.transform.rotate(fog_surf, 90), (24, display.get_height()))
        display.blit(pygame.transform.flip(side_fog, False, True), (-6, 0))
        display.blit(side_fog, (0, 0))
        display.blit(pygame.transform.flip(side_fog, True, True), (display.get_width() - 24, 0))
        display.blit(pygame.transform.flip(side_fog, True, False), (display.get_width() - 24 + 6, 0))
        game_time += 1

        if 0 < player.ghostEnergy < 100:
            visionoverlay.set_alpha(player.ghostEnergy)
            if player.ghostVision:
                for i in range(7):
                    xvel = random.randint(0, 20) / 10 - 1

                    particle = Particle((12, 230, 242), (120, 60), random.randint(2, 4), (240, 135), xvel, -2)
                particles.add(particle)


        #   camera_group.parallax_layers.append((particle, camera_group.speed_multipliers.get(particle.parallaxLayer, 1.0)))

        else:
            visionoverlay.set_alpha(105)

        if player.ghostVision:
            display.blit(pygame.transform.scale(visionoverlay, (WIDTH, HEIGHT)), (0, 0))
            for sprite in tileHandler:
                sprite.handle_ghost_vision(display)

        else:
            for sprite in tileHandler:
                sprite.no_ghost_vision()

        for thingy in particles:
            thingy.draw(display)
            thingy.update()
            if len(pygame.sprite.spritecollide(particle, camera_group, False)) > 0:
                thingy.bounce()

        font.render(surf=display, text="energy", color=(255, 255, 255), loc=(5, 5), scalefactor=1,
                    outlinecolor=(12, 230, 242), outline=True)

        for i in range(int((player.ghostEnergy // 80) + 0.5)):
            display.blit(pygame.transform.rotate(energyImage, somerot), (energyImage.get_width() * i, 10))
        somerot -= 1
        screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0, 0))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    menu()
