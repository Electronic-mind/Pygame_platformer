import pygame
import sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = [600, 400]

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption("Happy national day!")

#display = pygame.Surface((300, 200))




#loading the map from game_map.txt
def load_map(path):
    f = open(path, 'r')
    data = f.read()
    f.close
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map("game_map.txt")


#load the image of the player
player_image = pygame.image.load("Saudi_lady-32bit.png")

#load the images of the tiles
grass_image = pygame.image.load("Grass_new.png")
dirt_image = pygame.image.load("Dirt_new.png")
TILE_SIZE = grass_image.get_width()




#checking for collisions
def collision_test(rects, tiles):
    hit_list = []
    for tile in tiles:
        if rects.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        if movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True

    return rect, collision_types


moving_l = False
moving_r = False


player_y_momentum = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
air_timer = 0

#scrolling the screen
true_scroll = [0,0]
scroll = true_scroll.copy()
scroll[0] = true_scroll[0]
scroll[1] = true_scroll[1]



while True:

    scroll[0] += (player_rect.x - scroll[0] - 284)/ 20
    scroll[1] += (player_rect.y - scroll[1] - 200)/ 20

    screen.fill((135, 206, 235))
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                screen.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                screen.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_r:
        player_movement[0] += 5
    if moving_l:
        player_movement[0] -= 5
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum += 2

    screen.blit(player_image, [player_rect.x - scroll[0], player_rect.y - scroll[1]])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moving_l = True
            if event.key == K_RIGHT:
                moving_r = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moving_l = False
            if event.key == K_RIGHT:
                moving_r = False

    #surf = pygame.transform.scale(display, WINDOW_SIZE)
    #screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)
