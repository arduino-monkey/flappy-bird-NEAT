import pygame, sys, random, neat, os

pygame.init()
pygame.font.init()
WIDTH = 432
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')


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

    animationTime = 100
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
        if self.movement <= 3:#flaps only if gowing up 
            if self.index < 2:
                self.index += 1
            else:
                self.index = 0


    def collide(self, pipe):
        bottomCollision = self.rect.colliderect(pipe.bottomRect)
        topCollision =  self.rect.colliderect(pipe.topRect)
        if topCollision or bottomCollision:
            return True
        else:  
            return False
    
    def boundary(self):
        if self.rect.top <= -100 or self.rect.bottom >= Floor.y:
            return True
        else:
            return False

class Pipe:
    gap = 200
    vel = 3

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

class Floor:
    x = 0
    y = 675
    vel = 3
    def move(self):
        if Floor.x <= -WIDTH:
            Floor.x = 0
        else:
            Floor.x -= Floor.vel
    
    def draw(self, screen):
        screen.blit(floorSurface, (Floor.x,Floor.y))
        screen.blit(floorSurface, (Floor.x + WIDTH, Floor.y))


def main(genomes, config):
    nets = []
    birds = []
    ge = []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(50, WIDTH/2))
        ge.append(genome)

    floor = Floor() 
    pipes = [Pipe(WIDTH)]
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run and len(birds):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                break
            
            if event.type == Bird.BIRDFLAP:
                for bird in birds:
                    bird.animate()

        pipeIndex = 0
        if len(birds):
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipeWidth:
                pipeIndex = 1 
        
        for i, bird in enumerate(birds):
            ge[i].fitness += 0.03
            bird.move()
            topPipeDist = abs(bird.y - pipes[pipeIndex].topPipeY)
            bottomPipeDist = abs(bird.y - pipes[pipeIndex].bottomPipeY)
            output = nets[i].activate((bird.y, topPipeDist ,bottomPipeDist))

            if output[0] > 0.5:
                bird.jump()
        floor.move()


        rem = []
        addPipe = False
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if bird.collide(pipe):
                    birdIndex = birds.index(bird)
                    ge[birdIndex].fitness -= 1
                    nets.pop(birdIndex)
                    ge.pop(birdIndex)
                    birds.pop(birdIndex)

            if pipe.x + pipeWidth < 0:
                rem.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                addPipe = True
        
        if addPipe:
            score += 1
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(WIDTH))
        
        for r in rem:
            pipes.remove(r)
        

        for bird in birds:
            if bird.boundary():
                birdIndex = birds.index(bird)
                nets.pop(birdIndex)
                ge.pop(birdIndex)
                birds.pop(birdIndex)
            
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

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to x generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)