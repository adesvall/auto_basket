import pygame as pg
from random import random, randint, choice
from collections import deque
# from panier import Panier

g = 9.81

class Ball():
    def __init__(self, panier = None) -> None:
        self.lance()
        self.rayon = 50
        self.panier = panier
        self.ancrage = None
        self.prevision = deque()

    def lance(self):
        self.center = pg.Vector2([randint(0, 1920), randint(1080 // 3, 1080 // 2)])
        self.shadow = self.center.copy()
        self.t = 0
        self.sens = -1 if self.center[0] > 1920 / 2 else 1
        self.speed = pg.Vector2([self.sens * (random() * 10 + 10), -20])

    def futur(self):
        if self.prevision:
            return self.prevision[-1]
        return self.center

    def simulate(self):
        # if self.prevision:
        #     print(self.center, self.prevision[0])
        if self.prevision and self.prevision[0] == self.center:
            # print("prevision")
            self.prevision.popleft()
            if self.prevision:
                return self.prevision[-1]
        # print("simul")
        self.prevision.clear()
        copy = Ball()
        copy.center = self.center.copy()
        copy.speed = self.speed.copy()
        for i in range(200):
            if abs(copy.speed.angle_to(pg.Vector2(0, 1))) < 40 and copy.speed.length() > 20:
                return copy.center
            copy.update()
            self.prevision.append(copy.center.copy())
        return copy.center

    def update(self):
        # if self.ancrage is not None:
        #     return
        self.t += 1
        self.center += self.speed
        self.speed += pg.Vector2([0, 0.13]) * g
        self.speed *= 0.99
        if self.center[1] + self.rayon >= 1080:
            self.speed[1] = -self.speed[1] * 1.02
            self.center[1] = 1080 - self.rayon
        if self.center[0] + self.rayon >= 1920:
            self.speed[0] = -self.speed[0] * 0.9
            self.center[0] = 1920 - self.rayon
        if self.center[0] - self.rayon <= 0:
            self.speed[0] = -self.speed[0] * 0.9
            self.center[0] = self.rayon
        if self.panier:
            c = self.panier.position - pg.Vector2([self.rayon, 0])
            if self.center[0] > self.panier.position[0]:
                c = self.panier.position + pg.Vector2([self.rayon, 0])
            if (c - self.center).length() < self.rayon:
                axe = (self.center - c).normalize()
                bounce = (self.speed - self.panier.speed).dot(axe) * axe
                self.speed -= 1.6 * bounce
                self.center = c + axe * self.rayon
            
            if self.panier.check_goal(self):
                return True
        return False
    
        
    def draw(self, zone):
        # if len(self.prevision) > 1:
        #     pg.draw.lines(zone, pg.Color("grey"), False, list(self.prevision), 3)
        #     pg.draw.circle(zone, pg.Color("black"), self.futur(), 5)
        pg.draw.circle(zone, pg.Color("orange"), self.center, self.rayon)
        if self.t > 10:
            self.t = 10
            self.shadow += pg.Vector2([0, 100])
        pg.draw.circle(zone, pg.Color("black"), self.shadow, self.rayon * 0.8)
        pg.draw.line(zone, pg.Color("black"), self.shadow + pg.Vector2([0, 80]), self.shadow + pg.Vector2([0, 400]), 60)
        shoulders = self.shadow + pg.Vector2([self.sens * 20, 90])
        pg.draw.line(zone, pg.Color("black"), shoulders, shoulders + pg.Vector2([0, -150]).rotate(self.sens * self.t * 18), 30)
