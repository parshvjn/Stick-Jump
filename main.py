import pygame, sys, random, math
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
            'player/damage': Animation(load_images('player/damage', scaleFactor=[50/24 + 0.75, 100/31]), img_dur=15),
            'bg1': Animation(load_images('bgs/bg1', scaleFactor= [WINW/480, WINH/270]), img_dur=2),
            'bg2': Animation(load_images('bgs/bg2', scaleFactor= [WINW/480, WINH/270]), img_dur=2),
            'grass': load_image('grass.png', [self.terrain.width/16, self.terrain.height/15])
        }
        self.player = Player(self.win, self)
        self.movementH = [False, False]
        self.clock = pygame.time.Clock()
        self.bgNum = math.ceil(random.randint(1, 20)/10)
        self.animation = self.assets[f'bg{self.bgNum}'].copy()
        self.tColor = (0,0,0) if self.bgNum == 1 else (255,255,255)
        pygame.mouse.set_cursor(*pygame.cursors.tri_right)
        self.score = 0
        with open('data.txt', 'r') as r:
            t = r.read()
            r.close()
            self.highScore = int(t.split(':')[-1])
         
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
            self.win.blit(self.animation.img(), (0, 0))
            self.animation.update()
            self.player.update(movement=[self.dist[0][0] if self.dist[0][0] < 0 else 0, 0], distAway=self.dist[1])
            self.player.render()
            self.terrain.update()
            self.terrain.render()
            text(self.win, 'FPS: ' + str(round(self.clock.get_fps())), (10, 10), self.tColor)
            text(self.win, f'Score: {self.score}', (WINW - len(str(self.score))*22 - 90, 10), self.tColor)
            text(self.win, f'High Score: {self.highScore}', (WINW - len(str(self.highScore))*22 - 170, 35), self.tColor)
            self.score += 1 if self.player.fall != True else 0
            self.clock.tick(120)
            # print(self.clock.get_fps())
            pygame.display.update()
        pygame.quit()
        

if __name__ == '__main__':
    program = Game()
    program.main()