import pygame
import random as rnd


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


class game3env():
    def __init__(self):
        pass

    def reset(self):
        pygame.init()
        self.win_size = 600
        self.win = pygame.display.set_mode((self.win_size, self.win_size))
        self.p = player()
        self.ap = apple(self.win_size)
        self.t = 0
        self.run = True

    def step(self, action=0):
        self.t += 1
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

        self.p.step(self.win_size)
        k = pygame.key.get_pressed()
        if self.p.y == 30:
            if (k[pygame.K_SPACE] or k[pygame.K_UP]):
                self.p.vy += 30
            if k[pygame.K_RIGHT]:
                self.p.vx += 5
            if k[pygame.K_LEFT]:
                self.p.vx -= 5

        if self.p.y < 30:
            self.p.y = 30
            self.p.vy = 0

        if self.ap.hit(self.p.x,self.p.y):
            self.ap.reset(self.win_size)

    def render(self):
        self.win.fill((0, 0, 0))
        self.p.draw(self.win, self.win_size)
        self.ap.draw(self.win,self.win_size)
        pygame.display.update()

    def close(self):
        pygame.quit()


a = game3env()
a.reset()
while True:
    if not a.run:
        break
    a.step()
    a.render()
a.close()
print(1)