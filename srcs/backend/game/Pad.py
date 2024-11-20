class Pad:
    def __init__(self, id, player_id=0, x=0, y=0, vx=0, vy=5, h=0, w=0, score=0):
        self.player_id = player_id
        self.id = id
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.h = h
        self.w = w
        self.score = score

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'h': self.h,
            'w': self.w,
            'score': self.score
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            player_id=data['player_id'],
            id=data['id'],
            x=data['x'],
            y=data['y'],
            vx=data['vx'],
            vy=data['vy'],
            h=data['h'],
            w=data['w'],
            score=data['score']
        )
    
    def __str__(self):
        return f"Pad {self.identifier} - Position ({self.x}, {self.y})"

    def init_2vs2(self):
        self.y = self.y / 2
        if self.id == 'C' or self.id == 'D':
            self.y = self.y * 3

    def init_4players(self, width, height):
        self.x = width / 2
        self.y = 10
        
        w = self.w
        self.w = self.h
        self.h = w

        if self.id == 'D':
            self.y = height - 10

    def set_player_id(self, player_id):
        self.player_id = player_id

    def score_up(self):
        self.score += 1

    def update(self, dir, vy):
        for i in range(vy):
            if dir == 'up':
                self.y -= 1
            else:
                self.y += 1
