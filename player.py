import pygame, math
class Player:
    def __init__(self, surface):
        self.pos = [300, 100]
        self.velocity = [0, 0]
        self.gravity = 1
        self.surf = surface
        self.speed = 2
        self.moveDist = 50
        self.shapex, self.shapey = 50, 100
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.shapex, self.shapey)
        
    def testJump(self):
        self.velocity[1] -= 2.15
    
    def update(self,movement = [0,0], distAway = [0,0]): 
        self.frame_movement = (((self.moveDist-movement[0] if movement[0] != 0 and distAway <= ((math.sqrt((2*(self.moveDist**2))))*1.35) else 0) / 75) + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += self.frame_movement[0]
        self.pos[1] += self.frame_movement[1]
        self.velocity[1] = 0 if movement[1] > 0 else min(5, self.velocity[1]+0.010)
        if self.pos[1] >= 650:
            self.velocity[1] = 0
            # self.pos[1] = 650-self.shapey
        # print(self.velocity)
        # print('pos', self.pos)
        # print('velocity:', self.velocity)
        print(self.frame_movement)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50, 100)

    def render(self):
        pygame.draw.rect(self.surf, (255, 0, 0), self.rect)
        # print(self.pos)