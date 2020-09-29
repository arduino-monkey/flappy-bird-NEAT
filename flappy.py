import pygame, sys, random

pygame.init()
WIDTH = 432
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
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
bird2 = pygame.image.load('assets/yellowbird-upflap.png')

bird0 = scaleSurface(bird0)
bird1 = scaleSurface(bird1)
bird2 = scaleSurface(bird2)

birdImages = [bird0,bird1,bird2]

class Bird:
    images = birdImages
    gravity = 0.25

    animationTime = 200
    BIRDFLAP = pygame.USEREVENT
    pygame.time.set_timer(BIRDFLAP, animationTime)


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movement = 0
        self.index = 0
        self.surface = Bird.images[self.index]
        self.rect = self.surface.get_rect(center = (self.x,self.y))
    
    def move(self):
        self.movement += Bird.gravity
        self.rect.centery += self.movement
    
    def jump(self):
        self.movement = 0
        self.movement -= 5
    
    def draw(self, screen):
        self.surface = Bird.images[self.index]
        screen.blit(self.rotate(), self.rect)
    
    def rotate(self):
        newSurface = pygame.transform.rotozoom(self.surface, -self.movement * 5, 1)
        return newSurface
    
    def animate(self):
        if self.movement <= 5:
            if self.index < 2:
                self.index += 1
            else:
                self.index = 0
        
    

bird0 = Bird(50,HEIGHT/2)
bird1 = Bird(150,HEIGHT/2)
bird2 = Bird(250,HEIGHT/2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                bird0.jump()
                bird1.jump()
                bird2.jump()
        
        if event.type == Bird.BIRDFLAP:
            bird0.animate()
            bird1.animate()
            bird2.animate()
    bird0.move()
    bird1.move()
    bird2.move()

    screen.blit(bgSurface,(0,0))

    bird0.draw(screen)
    bird1.draw(screen)
    bird2.draw(screen)
    pygame.display.flip()
    clock.tick(100)
