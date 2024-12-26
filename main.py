import pygame, sys
from constants import *
from player import *
from utils import *
from terrain import *

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINW,WINH))
        self.running = True
        self.terrain = Terain(self.win, self)
        self.assets = {
            'player/idle1': Animation(load_images('player/idle1', scaleFactor=[50/18, 100/30]), img_dur=15),
            'player/idle2': Animation(load_images('player/idle2', scaleFactor=[80/30, 100/33]), img_dur=15),
            'player/idle3': Animation(load_images('player/idle3', scaleFactor=[50/19, 100/31]), img_dur=15),
            'player/walk': Animation(load_images('player/walk', scaleFactor=[50/22 + 0.25, 100/31]), img_dur=10),
            'player/run': Animation(load_images('player/run', scaleFactor=[50/20 + 0.25, 100/32]), img_dur=10),
            'player/jump': Animation(load_images('player/jump', scaleFactor=[50/19 + 0.25, 100/30]), img_dur=10, loop=False),
            'player/fall': Animation(load_images('player/fall', scaleFactor=[50/19 + 0.5, 100/30]), img_dur=10, loop=False),
            'grass': load_image('grass.png', [self.terrain.width/16, self.terrain.height/15])
        }
        self.player = Player(self.win, self)
        self.movementH = [False, False]
        self.clock = pygame.time.Clock()
         
    def main(self):
        while self.running:
            self.win.fill(BGCOLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.testJump()
                    if event.key == pygame.K_LEFT:
                        self.movementH[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movementH[1] = True
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movementH[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movementH[1] = False
            
            self.dist = distance(self.player.rect.centerx, pygame.mouse.get_pos()[0], self.player.rect.centery, pygame.mouse.get_pos()[1], [self.player.shapex/2, self.player.shapey/2], self.player.moveDist)
            # print('dist:', self.dist)
            self.player.update(movement=[self.dist[0][0] if self.dist[0][0] < 0 else 0, 0], distAway=self.dist[1])
            self.player.render()
            self.terrain.update()
            self.terrain.render()
            self.clock.tick(120)
            # print(self.clock.get_fps())
            pygame.display.update()
        pygame.quit()
        

if __name__ == '__main__':
    program = Game()
    program.main()