import pygame, sys, random

pygame.init()
WIDTH = 432
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def scaleSurface(surface):
    times = 1.5
    scaledWidth = round(surface.get_width()*times)
    scaledHeight = round(surface.get_height()*times)
    return pygame.transform.scale(surface, (scaledWidth, scaledHeight))



bgSurface = pygame.image.load('assets/background-night.png')
bgSurface = scaleSurface(bgSurface)

floorSurface = pygame.image.load('assets/base.png')
floorSurface = scaleSurface(floorSurface)
floorXPos = 0


def drawFloor():
    screen.blit(floorSurface, (floorXPos,675))
    screen.blit(floorSurface, (floorXPos + WIDTH,675))


class Bird:
    pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(bgSurface,(0,0))
    floorXPos -= 1
    drawFloor()
    if floorXPos <= -WIDTH:
        floorXPos = 0
    pygame.display.flip()
    clock.tick(100)
