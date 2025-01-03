import pygame, math
from constants import *
import random
from utils import *

class Player:
    def __init__(self, surface, game):
        self.game = game
        self.spawn = [self.game.terrain.width*3, WINH - self.game.terrain.height - self.game.assets['player/idle1'].img().get_height() - 100]
        self.pos = [self.game.terrain.width*3, WINH - self.game.terrain.height - self.game.assets['player/idle1'].img().get_height() - 100]
        self.velocity = [0, 0]
        self.gravity = 1
        self.surf = surface
        self.speedDividor = 200 # the more, the slower the palyer is pushed on horizontal axis by cursor
        self.moveDist = 50
        self.shapex, self.shapey = self.game.assets['player/idle1'].img().get_width(), self.game.assets['player/idle1'].img().get_height()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.shapex, self.shapey)
        self.floory = TOPY - self.shapey -2
        self.jump = True
        self.action = ''
        self.set_action(f'idle{random.randint(1, 3)}')
        self.idleReset = True
        self.fall = False
        self.deathAnim = False
        self.deathCount = 0
        self.reset = False
        self.resetDur = 3
        self.deathCount1 = 0
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets['player/' + self.action].copy()
        
    def testJump(self):
        if self.fall == False:
            self.velocity[1] -= 3 if self.jump else 0
            self.jump = False
            self.set_action('jump')
            self.idleReset = True
    
    def deathReset(self):
        self.pos = [self.game.terrain.width*3, WINH - self.game.terrain.height - self.game.assets['player/idle1'].img().get_height() - 100]
        self.set_action('idle1')
        self.game.terrain.tiles = [[x*self.game.terrain.width, self.game.terrain.topY] for x in range(TILESONSCREEN)]
        self.fall = False
        self.deathAnim = False
        self.deathCount = 0
        self.reset = False
        self.deathCount1 = 0
        self.velocity = [0, 0]
        self.game.highScore = max(self.game.score, self.game.highScore)
        save(self.game.highScore)
        print(self.game.score, self.game.highScore)
        self.game.score = 0


    
    def update(self,movement = [0,0], distAway = [0,0]):
        self.frame_movement = ((((self.moveDist-movement[0] if movement[0] != 0 and distAway <= ((math.sqrt((2*(self.moveDist**2))))*1.35) else 0) / self.speedDividor) if movement[0] > -73 else 0) + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += self.frame_movement[0] if self.deathAnim == False else 0
        self.pos[1] += self.frame_movement[1] if self.deathAnim == False else 0
        # print(movement[0])
        self.velocity[1] = 0 if movement[1] > 0 else min(5, self.velocity[1]+0.020)
        if self.pos[1] >= self.floory and self.fall == False:
            self.velocity[1] = 0
            self.pos[0]-=SPEED if self.frame_movement[0] == 0 else 0
            self.jump = True
            if self.frame_movement[0] != 0 and movement[0] > -73:
                if movement[0] < -60 and self.action != 'run': self.set_action('walk')
                else: self.set_action('run')
                self.idleReset = True

            if self.frame_movement[0] == 0 and movement[0] < -75 or movement[0] == 0 and self.frame_movement[0] == 0:
                if self.idleReset: self.set_action(f'idle{math.ceil(random.randint(1, 30)/10)}'); self.idleReset = False
            
            #death
            for i, tile in enumerate(self.game.terrain.tiles):
                if tile[0] + self.game.terrain.width < self.pos[0] and self.game.terrain.tiles[i+1][0] > self.pos[0] + self.shapex:
                    self.fall = True
                    self.set_action('fall')


        if self.velocity[1] > 0 and self.deathAnim == False:
            self.set_action('fall')

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.animation.img().get_size()[0], self.animation.img().get_size()[1])
        self.shapex, self.shapey = self.animation.img().get_size()[0], self.animation.img().get_size()[1]

        # death
        if self.pos[0] + self.shapex <= 0 or self.pos[0] >= WINW - 5:
            self.deathReset()
        
        if self.pos[1] + self.shapey + (5 if self.deathCount == 0 else 15) >= WINH and self.reset != True:
            if self.deathCount == 0:
                self.deathAnim = True
                self.set_action('damage')
                self.game.terrain.tiles = []
                self.timer = Timer(2)
                self.returnX, self.returnY = self.pos[0] - self.spawn[0], self.pos[1] - self.spawn[1]
            else:
                if self.timer.count():
                    self.reset = True
            self.deathCount += 1
        
        if self.reset:
            if self.pos[0] <= self.spawn[0] and self.pos[1] <= self.spawn[1]:
                if self.deathCount1 == 0: self.timer1 = Timer(1)
                else:
                    if self.timer1.count():
                        self.deathReset()

                self.deathCount1 += 1

            else:
                self.pos[0] -= self.returnX/self.resetDur/30
                self.pos[1] -= self.returnY/self.resetDur/30

        self.animation.update()

    def render(self):
        self.game.win.blit(self.animation.img(), self.pos)
        # print(self.pos)

 
#make difficulty levels (speed chagne and if edges make you fall or not (high difficulty --> hiegher amount of edge that makes you fall))
#achevientmenst to add (random section, reach the ONE block !!! (also add diff image for the one block that maybe lookes diff (and put img of blockj on acheivement popup))
#another acheivement: impossible jump (unlucky) which is a jump of too many blocks that happens soemtimes that isnt possible
#anotyher ahceivement: if person barely makes it on edge (for each level where the edges are shorter (Edge Master I, II, etc..))
#ahvievnemetns for scores

#list of priority
# 1. finish this game (basic ~ no addons)
# 2. Learn C++
# 3. Add on to this game :) ~ add starting menu, and achveiemetns and upgrades
