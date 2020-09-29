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


bird0 = pygame.image.load('assets/yellowbird-downflap.png') 
bird1 = pygame.image.load('assets/yellowbird-midflap.png')
bird2 = pygame.image.load('assets/yellowbird-downflap.png')

bird0 = scaleSurface(bird0)
bird1 = scaleSurface(bird1)
bird2 = scaleSurface(bird2)

birdImages = [bird0,bird1,bird2]

class Bird:
    images = birdImages
    animationTime = 200
    gravity = 0.25

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.birdMovement = 0
        self.index = 0
        self.surface = Bird.images[0]
        self.rect = self.surface.get_rect(center = (self.x,self.y))
    
    def move(self):
        self.birdMovement += Bird.gravity
        self.rect.centery += self.birdMovement
    
    def jump(self):
        self.birdMovement = 0
        self.birdMovement -= 5
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)


bird = Bird(50,HEIGHT/2)
bird1 = Bird(100,HEIGHT/2)
bird2 = Bird(150,HEIGHT/2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
                bird1.jump()
                bird2.jump()
    bird.move()
    bird1.move()
    bird2.move()

    screen.blit(bgSurface,(0,0))

    bird.draw(screen)
    bird1.draw(screen)
    bird2.draw(screen)
    pygame.display.flip()
    clock.tick(100)
