import pygame
from constants import *
import random

class Terain:
    def __init__(self, window, game):
        self.topY = TOPY
        self.height = WINH - TOPY
        self.width = WINW / TILESONSCREEN
        self.tiles = []
        self.win = window
        self.tiles = [[x*self.width, self.topY] for x in range(TILESONSCREEN)]
        self.speed = SPEED
        self.game = game
        # print(self.tiles)

    def update(self):
        # when first tile off screen then add blocks and as they leave compeltely remove
        for tiles in self.tiles:
            tiles[0] -= self.speed
            if tiles[0] + self.width < 0:
                self.tiles.remove(tiles)
        
        if len(self.tiles) != 0:
            if self.tiles[-1][0] + self.width <= WINW:
                n = random.randint(3, 7) # how big of a gap of air
                npos = random.randint(0, TILESONSCREEN/2 - n) #where in the first half to start gap
                i = random.randint(3, 8)
                ipos = random.randint(TILESONSCREEN/2, TILESONSCREEN - i)
                t = [[x*self.width + WINW - (50 - self.tiles[1][0]), self.topY] for x in range(TILESONSCREEN)]
                del t[npos:npos+n]
                del t[ipos:ipos+i]
                for tile in t:
                    self.tiles.append(tile)
                # print(self.tiles)

    def render(self):
        for tile in self.tiles:
            self.win.blit(self.game.assets['grass'], (tile[0], tile[1]))
            # pygame.draw.rect(self.win, (0,0,255), pygame.Rect(tile[0], tile[1], self.width, self.height))