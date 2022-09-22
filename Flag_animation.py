import pygame, sys
from pygame.locals import *




class AnimatedObj(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("Flag1.png"))
        self.sprites.append(pygame.image.load("Flag2.png"))
        self.sprites.append(pygame.image.load("Flag3.png"))
        self.sprites.append(pygame.image.load("Flag4.png"))
        self.sprites.append(pygame.image.load("Flag5.png"))
        self.sprites.append(pygame.image.load("Flag6.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self, speed):
        self.current_sprite += speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]



#Initializing pygame
pygame.init()


#Setting the cclock and FPS
clock = pygame.time.Clock()
FPS = 60


#Creating a display surface
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


#creating the sprites
moving_sprites = pygame.sprite.Group()
Flag = AnimatedObj(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
moving_sprites.add(Flag)


#Creating the mast
mast_image = pygame.image.load("mast.png")
mast_rect = mast_image.get_rect()
mast_rect.topleft = [WINDOW_WIDTH//2 - 132, WINDOW_HEIGHT//2 -80]




#Main loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    #Update the screen
    
    surface.fill((0, 0, 0))
    surface.blit(mast_image, mast_rect)
    moving_sprites.draw(surface)
    moving_sprites.update(0.15)
    pygame.display.flip()
    clock.tick(FPS)




