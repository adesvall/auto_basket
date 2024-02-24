import pygame as pg

class Panier():
    def __init__(self, bot=None) -> None:
        self.position = pg.Vector2([1920/2, 1080/2])
        self.speed = pg.Vector2([0, 0])
        self.acc = pg.Vector2([0, 0])
        self.rayon = 75
        self.score = 0
        self.bot = bot

    def check_goal(self, ball):
        if (ball.center - self.position).length() < self.rayon/4 and ball.center[1] > self.position[1]:
            if ball.speed[1] > self.speed[1]:
                self.score += 1
            else:
                self.score -= 1
            ball.lance()
            return True
        return False

    def update(self, ball):
        ball.simulate()
        if self.bot:
            self.acc = self.bot.decide_acc(ball.center, ball.speed, self.position, self.speed)
            self.speed += self.acc / 100
            self.speed *= 0.9
            self.position += self.speed
            return
        if (ball.center - self.position - pg.Vector2(0, 100)).length() > 300 or ball.center[1] > self.position[1]:
            self.position = (self.position * 0.9 + self.target * 0.1)
    
    def draw(self, zone):
        # pg.draw.line(zone, pg.Color("blue"), self.position, self.position - self.acc / 5, 15)
        # pg.draw.circle(zone, pg.Color("black"), self.target, 5)
        pg.draw.rect(zone, pg.Color("gray"), pg.Rect(
            self.position - pg.Vector2([3*self.rayon, 3*self.rayon]),
            pg.Vector2([self.rayon*6, 3.2*self.rayon])
        ), border_radius=10)
        pg.draw.rect(zone, pg.Color("white"), pg.Rect(
            self.position - pg.Vector2([self.rayon, self.rayon*1.4+7]),
            pg.Vector2([self.rayon*2, self.rayon*1.4])
        ), width=15, border_radius=4)

        font = pg.font.Font(None, 100)
        img = font.render(str(self.score), True, pg.Color("white"))
        rect = img.get_rect()
        rect.center = self.position + pg.Vector2([0, -self.rayon*2])
        zone.blit(img, rect)
    
    def draw_arceau(self, zone):
        pg.draw.rect(zone, pg.Color("red"), pg.Rect(
            self.position - pg.Vector2([self.rayon, self.rayon/10]),
            pg.Vector2([self.rayon*2, self.rayon/5])
        ), border_radius=10)
    
    