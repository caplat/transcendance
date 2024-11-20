import random
import math


class Ball:
    def __init__(self, x=0, y=0, vx=0, vy=0, r=5, speed=5, state='pause'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.speed = speed
        self.state = state
        # self.beforeLast = ''
        # self.last = ''

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'r': self.r,
            'speed': self.speed,
            'state': self.state
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            x=data['x'],
            y=data['y'],
            vx=data['vx'],
            vy=data['vy'],
            r=data['r'],
            speed=data['speed'],
            state=data['state']
        )
    
    def __str__(self):
        return f"Ball {self.identifier} - Position ({self.x}, {self.y})"

    def reset(self, width, height):
        self.state = 'pause'
        self.x = width / 2
        self.y = height / 2
        self.vx = 0
        self.vy = 0

    def start(self):
        angle = random.uniform(-math.pi, math.pi)
        
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

        self.state = 'start'
        print(f'ANGLE {angle}, VX : {self.vx}, VY : {self.vy}')

    def change_dir(self, pad):
        dx = self.x - pad.x
        dy = self.y - pad.y
        angle = math.atan2(dy, dx)  # Angle en radians

        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed
        print(f'CHANGE DIR')

    def check_collide_pad(self, pad):
        pad_half_width = pad.w / 2
        pad_half_height = pad.h / 2

        distance_x = abs(self.x - pad.x)
        distance_y = abs(self.y - pad.y)

        if distance_x > (pad_half_width + self.r):
            return False

        if distance_y > (pad_half_height + self.r):
            return False

        if distance_x <= pad_half_width:
            return True
        if distance_y <= pad_half_height:
            return True

        corner_distance_sq = (distance_x - pad_half_width) ** 2 + (distance_y - pad_half_height) ** 2
        return corner_distance_sq <= self.r ** 2

    def update(self, padA, padB, height, width):
        if self.state != 'start':
            return

        vx = self.vx / self.speed
        vy = self.vy / self.speed
 
        i = 0
        while i < self.speed:
            i += 1

            x = self.x
            y = self.y

            self.x += vx 
            self.y += vy

            if self.y - self.r <= 0:
                self.y = self.r -(self.y - self.r)
                self.vy = -self.vy
                vy = -vy
            if self.y + self.r >= height:
                self.y = (height - self.r) + (height -(self.y + self.r))
                self.vy = -self.vy
                vy = -vy
            
            if self.x - self.r <= 0 or self.x + self.r >= width:
                if self.x - self.r <= padA.w / 2:
                    padB.score_up()
                if self.x + self.r >= width - padB.w / 2:
                    padA.score_up()
                self.reset(width, height)
                return
            
            if self.check_collide_pad(padA):
                self.change_dir(padA)
                self.x = x
                self.y = y
                vx = self.vx / self.speed
                vy = self.vy / self.speed
                
                if self.check_collide_pad(padA):
                    self.x += vx
                    self.y += vy

            if self.check_collide_pad(padB):
                self.change_dir(padB)
                self.x = x
                self.y = y
                vx = self.vx / self.speed
                vy = self.vy / self.speed
                
                if self.check_collide_pad(padB):
                    self.x += vx
                    self.y += vy

