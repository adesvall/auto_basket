import pygame as pg
import numpy as np
from ball import Ball
from game import Game
from panier import Panier
from scipy.special import expit as sig

class Bot:
    def __init__(self, params=None) -> None:
        if params is None:
            self.params = np.random.uniform(-1, 1, 10).reshape(5, 2)
            self.params = np.array([[-2.1717437401190014, -5.3574203730907515],
                                    [-0.6303338701587174, 0.441696499800087],
                                    [0.005527558475786492, -0.8947433794664587],
                                    [0.05232651096475999, -0.013936618828040957],
                                    [0.00929586925461999, -0.011488106203661736],
                                    [15.42326237865405, -0.30976813668237996],
                                    [-3.8976347556063984, 13.381096669325121],
                                    [13.115898251177343, 1.8162294572950064],
                                    [-1.9970419544296527, 9.973805150263038],
                                    [-0.2558459111726316, -0.7999396414445237],
                                    [0.1985090823092533, -1.0593873890698435]])
            # self.params = np.array([[-2.276405847327988, -5.731710489044487], # Constant
            #                     [-0.8546297647482497, 0.8199539885180153], # Position X / center
            #                     [-0.4139069940516908, -0.4054331619164124], # Position Y / bas
            #                     [-0.4139069940516908, -0.4054331619164124], # Speed X
            #                     [-0.4139069940516908, -0.4054331619164124], # Speed Y
            #                     [15.249802848522409, 0.06970495520714629], # Position rel ball X
            #                     [-3.813764498303531, 13.242035057250256], # Position rel ball Y
            #                     [13.429715271838703, 1.818452798781599], # Speed rel ball X
            #                     [-2.012267265803445, 9.64973050661193], # Speed rel ball Y
            #                     [-0.1241175687438223, -0.64073704907828], # rel * rel_speed X
            #                     [0.17189519378098894, -0.6621594370899332], # rel * rel_speed Y
            # ]) 
        else:
            self.params = params.copy()
    
    def decide_acc(self, ball_pos, ball_speed, pos, speed):
        rel = np.array(ball_pos - pos)
        rel_speed = np.array(ball_speed - speed)
        x = np.concatenate([np.ones((1,)), pos - pg.Vector2(1920/2, 1080), speed, rel, rel_speed, np.abs(rel) * rel_speed]).reshape(1, -1)
        acc = sig(rel.dot(rel)**0.5 / 10) * np.dot(x, self.params).reshape(-1)
        acc = pg.Vector2(list(acc))
        acc = acc.normalize() * min(500, acc.length())
        # print(acc)
        return  acc

    def mutate(self, mutation_rate):
        # filter = np.zeros((11, 2), dtype=bool)
        # filter[0] = [True, True]
        # filter[2] = [True, True]
        # # print(filter)
        self.params += np.random.normal(0, mutation_rate, 22).reshape(-1, 2)
        self.params[0, 0] = 0

    
    def evaluate_fitness(self):
        panier = Panier(self)
        ball = Ball(panier=panier)
        score = 0
        for iter in range(1200):
            panier.update(ball)
            ball.update()
            # print(score)
            # print(ball.futur())
            score -= (panier.position - ball.futur()).length() / 1000
        return score + panier.score * 1000
        return - np.absolute(self.params - np.linspace(-10, 10, 6)).sum()
    
    def game(self):
        game = Game(Panier(bot=self))
        game.loop()

