import os
import random
import math
import pygame
from os import listdir, name
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("car game thing ")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 800, 600
FPS=60
PLAYER_VEL = 5


window = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y,width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
    
    def move(self, dx,dy):
        self.x_vel = +dx
        self.y_vel = +dy

    def move_left(self, vel):
        self.x_vel = -vel

    def move_right(self, vel):
        self.x_vel = vel
    
    def move_up(self, vel):
        self.y_vel = -vel

    def move_down(self, vel):
        self.y_vel = vel


    
    def loop(self,fps):
        self.move(self.x_vel, self.y_vel)
        self.update()

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

def get_background(name):
    #rearrange files and folders in assets then edit code below 
    image = pygame.image.load(join("assets", name))
    _,_, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH//width + 1):
        for j in range(HEIGHT//height + 1):
            pos = (i*width, j*height)
            tiles.append(pos)
    return tiles, image
        

def draw(window, background, bg_image, player, objects, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)

    pygame.display.update()

def handle_move(player):
    keys = pygame.key.get_pressed()

    player.y_vel = 0
    player.x_vel = 0
    if (keys[pygame.K_LEFT]) or (keys[pygame.K_a]):
        player.move_left(PLAYER_VEL)
    if (keys[pygame.K_RIGHT]) or (keys[pygame.K_d] ):
        player.move_right(PLAYER_VEL)
    if (keys[pygame.K_UP]) or (keys[pygame.K_w]):
        player.move_up(PLAYER_VEL)
    if (keys[pygame.K_DOWN]) or (keys[pygame.K_s]):
        player.move_down(PLAYER_VEL)


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Brown.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    

    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 150
    #blocks= [Block(0, HEIGHT - block_size, block_size)]

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_SPACE and player.jump_count < 2) or (event.key == pygame.K_UP and player.jump_count < 2) or (event.key == pygame.K_w and player.jump_count < 2):
                    player.jump() 


        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player, offset_x, offset_y)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.top - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or ((player.rect.bottom - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel
        

    pygame.quit()
    quit()

    
if __name__ == "__main__":
    main(window)