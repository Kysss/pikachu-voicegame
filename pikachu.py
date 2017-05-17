import math
import random
import cocos

class PIKACHU (cocos.sprite.Sprite):
    def __init__(self):
        super (PIKACHU, self).__init__('pikachu.png')
        self.can_jump = False
        self.speed = 0
        self.image_anchor = 0,0
        self.position = 100,300
        self.schedule(self.update)


    def jump (self, h):
        if self.can_jump:
            self.y+=2
            self.speed -= max(min (h, 10),7)
            self.can_jump = False

    def land (self,y):
        if self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y =y

    def update (self,dt):
        self.speed += 10 *dt
        self.y -= self.speed
        if self.y < -80:
            self.reset()


    def reset (self):
        self.parent.reset()
        self.can_jump = False
        self.speed = 0
        self.position = 100,300
