import pygame
import sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
icon = pygame.image.load("Saudi_map_icon.png")

WINDOW_SIZE = [600, 300]
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
pygame.display.set_caption("Happy national day!")






national_anthem = pygame.mixer.music

national_anthem.load("national_anthem.mp3")
national_anthem.play(-1, 0.0)
national_anthem.set_volume(0.4)

jump_sound = pygame.mixer.Sound("jump.wav")

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
player_image_right = pygame.image.load("Saudi_lady-right.png")
player_image_left = pygame.image.load("Saudi_lady-left.png")
city_background = pygame.image.load("city_image.png")
background_rect = city_background.get_rect()
background_rect.topleft = (0, 0)
background_image = pygame.Surface(WINDOW_SIZE)

#load the images of the tiles
grass_image = pygame.image.load("Grass.png")
dirt_image = pygame.image.load("Dirt.png")
TILE_SIZE = grass_image.get_width()

background_objects = [[0.25, [120, 10, 70, 400]], [0.5, [300, 30, 50, 200]]]


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

player_rect = pygame.Rect(400, 200, player_image_right.get_width(), player_image_right.get_height())

air_timer = 0

#scrolling the screen
true_scroll = [0,0]
scroll = true_scroll.copy()
scroll[0] = true_scroll[0]
scroll[1] = true_scroll[1]

direction = 1

while True:
    
    scroll[0] += (player_rect.x - scroll[0] - 284)/ 20
    scroll[1] += (player_rect.y - scroll[1] - 100)/ 20
    
    if player_rect.x <= 300:
        scroll[0] = 0
    
    screen.fill((135, 206, 235))
    screen.blit(city_background, background_rect)
    
    
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.25:
            pygame.draw.rect(screen, (14, 222, 150), obj_rect)
        else :
            pygame.draw.rect(screen, (9, 91,85), obj_rect)

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

    if player_rect.bottom > 400:
        player_rect.left = 400
        player_rect.top = 200

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['top']:
        player_y_momentum += 2

    
    if moving_l :
        direction = -1
    elif moving_r:
        direction = 1
        

    if direction == -1:
        screen.blit(player_image_left, [player_rect.x - scroll[0], player_rect.y - scroll[1]])

    elif direction == 1:
        screen.blit(player_image_right, [player_rect.x - scroll[0], player_rect.y - scroll[1]])

    
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
                jump_sound.play()
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
