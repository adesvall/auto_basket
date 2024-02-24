import pygame as pg
from ball import Ball
from panier import Panier
# from population import Population

class Game:
    def __init__(self, panier=Panier()) -> None:
        pg.init()
        self.zone = pg.display.set_mode((1920, 1080))
        pg.display.toggle_fullscreen()
        self.panier = panier
        self.ball = Ball(self.panier)
    
    def update(self):
        # pg.mouse.get_pos()
        self.panier.update(self.ball)
        self.ball.update()

    def draw(self):
        self.zone.fill(pg.Color("dark grey"))
        self.panier.draw(self.zone)
        self.ball.draw(self.zone)
        self.panier.draw_arceau(self.zone)
        pg.display.flip()


    def loop(self):
        while True:
            if pg.key.get_pressed()[pg.K_ESCAPE]:
                exit()
            for E in pg.event.get():
                if E.type == pg.QUIT:
                    print("quit")
                    pg.quit()
                    exit()
                if pg.mouse.get_pressed()[0]:
                    if self.ball.ancrage is None:
                        self.ball.ancrage = pg.Vector2(pg.mouse.get_pos())
                        # self.ball.center = self.ball.ancrage
                else:
                    if self.ball.ancrage is not None:
                        self.ball.speed = (self.ball.ancrage - pg.mouse.get_pos()) / 3
                        self.ball.ancrage = None

            self.update()
            self.draw()
            pg.time.Clock().tick(60)
