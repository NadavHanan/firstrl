import gym
from gym import spaces
import pygame
import random as rnd
import math
import numpy as np

class apple:
    def __init__(self, winsz):
        self.x= rnd.randint(21,winsz-11)
        self.y= rnd.randint(21,99)

    def draw(self, win, win_size):
        pygame.draw.rect(win, (255, 0, 0), (self.x, win_size - self.y, 10, 10))

    def hit(self, px, py):
        return  True if (px-10)<self.x<(px+20) and (py+10)>self.y>(py-20) else False

    def reset(self, winsz):
        self.x = rnd.randint(21, winsz - 11)
        self.y = rnd.randint(21, 99)


class player:
    def __init__(self, x=500):
        self.x = x
        self.y = 30
        self.vx = 0
        self.vy = 0

    def step(self, win_size, y=30):
        if self.x < 10:
            self.x = 10
            self.vx = 0
        elif self.x > (win_size - 30):
            self.x = win_size - 30
            self.vx = 0
        if self.y > y:
            self.vy -= 5
        elif self.y == y:
            if self.vx > 2:
                self.vx -= 3
            elif self.vx < -2:
                self.vx += 3
            else:
                self.vx = 0

        self.x += self.vx
        self.y += self.vy

    def draw(self, win, win_size):
        pygame.draw.rect(win, (255, 255, 255), (self.x, win_size - self.y, 20, 20))






class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-601, high=601,
                                            shape=(4,), dtype=np.float32)

    def step(self, action):
        self.t += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
        if self.t>1000:
          self.done = True

        self.p.step(self.win_size)
        
        if self.p.y == 30:
            if (action==1):
                self.p.vy += 30
            if action==2:
                self.p.vx += 5
            if action==3:
                self.p.vx -= 5

        if self.p.y < 30:
            self.p.y = 30
            self.p.vy = 0

        if self.ap.hit(self.p.x,self.p.y):
            self.ap.reset(self.win_size)
            self.prize = 1000000
        info = {}
        dx = self.p.x - self.ap.x
        dy = self.p.y - self.ap.y
        d = math.sqrt(dx**2 + dy**2)
        self.reward = (1000 - d + self.prize)//100
        self.prize = 0
        self.observation = [dx, dy, self.p.vx, self.p.vy]
        self.observation = np.array(self.observation)
        return self.observation, self.reward, self.done, info
    
    def reset(self):
        pygame.init()
        self.win_size = 600
        self.win = pygame.display.set_mode((self.win_size, self.win_size))
        self.p = player()
        self.ap = apple(self.win_size)
        self.t = 0
        self.done = False
        self.prize = 0
        dx = self.p.x - self.ap.x
        dy = self.p.y - self.ap.y
        self.observation = [dx, dy, self.p.vx, self.p.vy]
        self.observation = np.array(self.observation)
        return self.observation  # reward, done, info can't be included
    
    def render(self, mode='human'):
        pygame.time.delay(20)
        self.win.fill((0, 0, 0))
        self.p.draw(self.win, self.win_size)
        self.ap.draw(self.win,self.win_size)
        pygame.display.update()
    
    def close (self):
        pygame.quit()



