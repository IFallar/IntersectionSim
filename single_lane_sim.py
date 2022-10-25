from operator import truediv
from re import X
from tkinter.ttk import Scale
import pygame
import time
import math


def car(x, y):
    WIN.blit(CAR, (x, y))


ROAD = pygame.image.load("Assets/All Roads.png")
CAR = pygame.image.load("Assets/Car_scaled.png")

vel = 5
turn = 0
left = 4

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Road Sim")

run = True
clock = pygame.time.Clock()

#car stuff

carX = 355
carX2 = 386
carY = 650

while run: 
    clock.tick(60)

    WIN.blit(ROAD, (0, 0))

    if carY == 400:
        vel = 5
        turn = -.5

    carY -= vel
    carX -= turn

    car(carX, carY)
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
            break

pygame.QUIT

