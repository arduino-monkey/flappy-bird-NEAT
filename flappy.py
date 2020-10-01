try:
    import pygame, sys, random, neat
except ModuleNotFoundError as e:
    print(e)

pygame.init()
pygame.font.init()
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

FONT = pygame.font.SysFont('comicsans', 40)

bgSurface = pygame.image.load('assets/background-night.png')
bgSurface = scaleSurface(bgSurface)


floorSurface = pygame.image.load('assets/base.png')
floorSurface = scaleSurface(floorSurface)


bottomPipeSurface = pygame.image.load('assets/pipe-green.png')
bottomPipeSurface = scaleSurface(bottomPipeSurface)

topPipeSurface = pygame.transform.flip(bottomPipeSurface, False, True)

pipeHeight = topPipeSurface.get_height()
pipeWidth = topPipeSurface.get_width()

bird0 = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird1 = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird2 = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()

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
    
    def die(self):
        if  self.rect.top <= -100 or self.rect.bottom >= Floor.y:
            return True
        else:
            return False
    
    def animate(self):         
        if self.movement <= 3:#flaps only if gowing up 
            if self.index < 2:
                self.index += 1
            else:
                self.index = 0

class Pipe:
    gap = 200
    vel = 2

    def __init__(self, x):
        self.x = x
        self.passed = False
        #when referring to pipe Y co-ordintates I mean y of top left
        #if size of screen changes the values of the random function also need to change
        #can be derived through this formula
        #screenHeight - (pipeSurfaceHeight+gap b/w the pipes)
        self.topPipeY = -random.randint(88,392)
        self.bottomPipeY = pipeHeight + self.topPipeY + Pipe.gap
        
        self.topRect = topPipeSurface.get_rect(topleft=(self.x,self.topPipeY))
        self.bottomRect = bottomPipeSurface.get_rect(topleft=(self.x,self.bottomPipeY))

    def draw(self, screen):
        screen.blit(topPipeSurface, self.topRect)
        screen.blit(bottomPipeSurface, self.bottomRect)
    
    def move(self):
        self.x -= Pipe.vel
        self.topRect.left = self.x
        self.bottomRect.left = self.x
    
    def collide(self, bird):
        birdRect = bird.rect
        bottomCollision = birdRect.colliderect(self.bottomRect)
        topCollision =  birdRect.colliderect(self.topRect)       
        if  topCollision or bottomCollision:
            return True
        else:
            return False

class Floor:
    x = 0
    y = 675
    vel = 2
    def move(self):
        if Floor.x <= -WIDTH:
            Floor.x = 0
        else:
            Floor.x -= Floor.vel
    
    def draw(self, screen):
        screen.blit(floorSurface, (Floor.x,Floor.y))
        screen.blit(floorSurface, (Floor.x + WIDTH, Floor.y))





def run():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        'config-feedforward.txt')
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main ,50)

def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(50,384))
        ge.append(g)


    floor = Floor() 
    pipes = [Pipe(700)]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == Bird.BIRDFLAP:
                for bird in birds:
                    bird.animate() 
        # pipeIndex = 0
        # if len(birds):
        #     if len(pipes)>1 and birds[0].x > pipes[0].x + pipeWidth:
        #         pipeIndex = 1
        # else:
        #     break

        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            if pipes:
                output = nets[i].activate((bird.y, abs(bird.y-pipes[-1].topPipeY), abs(bird.y-pipes[-1].bottomPipeY)))
                if output[0] > 0.5:
                    bird.jump()
        floor.move()

        addPipe = False
        for pipe in pipes[:]:
            pipe.move
            for bird in birds[:]:
                if pipe.collide(bird) or bird.die():
                    birdIndex = birds.index(bird)
                    ge[birdIndex].fitness -= 1
                    birds.pop(birdIndex)
                    nets.pop(birdIndex)
                    ge.pop(birdIndex)
                
                if pipe.passed == False and pipe.x + pipeWidth < bird.x:
                    score += 1
                    pipe.passed = True
                    for g in ge:
                        g.fitness += 5
                    pipes.append(Pipe(WIDTH))            
            if pipe.x + pipeWidth < 0:
                pipes.remove(pipe)
                
        screen.blit(bgSurface,(0,0))         
        

        for pipe in pipes:
            pipe.draw(screen)
        floor.draw(screen)
        for bird in birds:
            bird.draw(screen)
        scoreText = FONT.render(f'Score: {score}', 1, (255,255,255))
        screen.blit(scoreText, (0,0))
        
        pygame.display.flip()
        clock.tick(100)
        print(len(birds))
run()