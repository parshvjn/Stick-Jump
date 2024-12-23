import pygame, sys
from constants import *
from player import *
from utils import *

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINW,WINH))
        self.running = True
        self.player = Player(self.win)
        self.movementH = [False, False]
         
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
            print('dist:', self.dist)
            self.player.update(movement=[self.dist[0][0] if self.dist[0][0] < 0 else 0, 0], distAway=self.dist[1])
            self.player.render()
            pygame.display.update()
        pygame.quit()
        

if __name__ == '__main__':
    program = Game()
    program.main()