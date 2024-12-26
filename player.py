import pygame, math
from constants import *
import random

class Player:
    def __init__(self, surface, game):
        self.game = game
        self.pos = [300, 100]
        self.velocity = [0, 0]
        self.gravity = 1
        self.surf = surface
        self.speedDividor = 50
        self.moveDist = 50
        self.shapex, self.shapey = self.game.assets['player/idle1'].img().get_width(), self.game.assets['player/idle1'].img().get_height()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.shapex, self.shapey)
        self.floory = TOPY - self.shapey
        self.jump = True
        self.action = ''
        self.set_action(f'idle{random.randint(1, 3)}')
        self.idleReset = True
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets['player/' + self.action].copy()
        
    def testJump(self):
        self.velocity[1] -= 2.50 if self.jump else 0
        self.jump = False
        self.set_action('jump')
        self.idleReset = True
    
    def update(self,movement = [0,0], distAway = [0,0]):
        self.frame_movement = ((((self.moveDist-movement[0] if movement[0] != 0 and distAway <= ((math.sqrt((2*(self.moveDist**2))))*1.35) else 0) / self.speedDividor) if movement[0] > -73 else 0) + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += self.frame_movement[0]
        self.pos[1] += self.frame_movement[1]
        print(movement[0])
        self.velocity[1] = 0 if movement[1] > 0 else min(5, self.velocity[1]+0.020)
        if self.pos[1] >= self.floory:
            self.velocity[1] = 0
            self.pos[0]-=SPEED if self.frame_movement[0] == 0 else 0
            self.jump = True
            if self.frame_movement[0] != 0 and movement[0] > -73:
                if movement[0] < -71 and self.action != 'run': self.set_action('walk')
                else: self.set_action('run')
                self.idleReset = True
        
            if self.frame_movement[0] == 0 and movement[0] < -75 or movement[0] == 0 and self.frame_movement[0] == 0:
                if self.idleReset: self.set_action(f'idle{math.ceil(random.randint(1, 30)/10)}'); self.idleReset = False

        if self.velocity[1] > 0:
            self.set_action('fall')

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.animation.img().get_size()[0], self.animation.img().get_size()[1])
        self.shapex, self.shapey = self.animation.img().get_size()[0], self.animation.img().get_size()[1]
        self.animation.update()

    def render(self):
        self.game.win.blit(self.animation.img(), self.pos)
        # print(self.pos)


#achevientmenst to add (random section, reach the ONE block !!! (also add diff image for the one block that maybe lookes diff (and put img of blockj on acheivement popup))