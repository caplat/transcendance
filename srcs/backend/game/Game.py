class Game:
    def __init__(self, width, height, type, state='init', users={}):
        self.width = width
        self.height = height
        self.state = state
        self.type = type
        self.users = users

    def to_dict(self):
        return {
            'width': self.width,
            'height': self.height,
            'state': self.state,
            'type': self.type,
            'users': self.users,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            width=data['width'],
            height=data['height'],
            state=data['state'],
            type=data['type'],
            users=data['users']
        )

    def __str__(self):
        return '{'f'"width": {self.width}, "height": {self.height}, "state": "{self.state}", "type": "{self.type}", "users": {self.users}''}'

    def set_user(self, id, user):
        self.users[id] = user

    def get_user(self, id):
        if id in self.users:
            return self.users[id]
        return None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_type(self):
        return self.type
