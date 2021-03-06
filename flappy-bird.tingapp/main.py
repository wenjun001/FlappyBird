from tingbot import *
import pygame
from pygame.locals import *
import sys
import random

def random_offset():
    return random.randint(50, 170)

class FlappyBird:
    def __init__(self):
        self.screen = screen.surface
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.background = pygame.image.load("background.png").convert()
        self.birdSprites = [pygame.image.load("1.png").convert_alpha(), pygame.image.load("2.png").convert_alpha(), pygame.image.load("dead.png")]
        self.wallUp = pygame.image.load("bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("top.png").convert_alpha()
        self.gap = 60
        self.wallx = 320
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random_offset()

    def updateWalls(self):  
        self.wallx -= 3
        if self.wallx < -80:
            self.wallx = 320
            self.counter += 1
            self.offset = random_offset()

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2

        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx, 220 + self.gap - self.offset + 10, self.wallUp.get_width() - 10, self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx, 0 - self.gap - self.offset - 10, self.wallDown.get_width() - 10, self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if self.bird[1] > 260:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 320
            self.offset = random_offset()
            self.gravity = 5
        
    def do_jump(self):
        if not self.dead:
            self.jump = 17
            self.gravity = 5
            self.jumpSpeed = 10

    def step(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         sys.exit()
        #     if event.type == pygame.KEYDOWN and not self.dead:
        #         self.jump()

        self.screen.fill((255,255,255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.wallUp, (self.wallx, 220 + self.gap - self.offset)) 
        self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
        screen.text(
            self.counter,
            xy=(160,40),
            color='white')
        if self.dead:
            self.sprite = 2
        elif self.jump:
            self.sprite = 1
        self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
        if not self.dead:
            self.sprite = 0
        self.updateWalls()
        self.birdUpdate()
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while True:
            clock.tick(30)
            self.step()

fb = FlappyBird()

@every(seconds=1.0/30)
def step():
    fb.step()

@left_button.down
@right_button.down
@midleft_button.down
@midright_button.down
def button_press():
    fb.do_jump()

run()
