import json
import uuid
import asyncio
import redis.asyncio as aioredis

from channels.generic.websocket import AsyncWebsocketConsumer

from .consumers import GameConsumer
from .Game import Game
from .Pad import Pad
from .Ball import Ball
from .utils import update_score


class OneVsOneConsumer(GameConsumer):
    async def connect(self):
        print("CONSUMER")

        await super().connect()
        print("1vs1 game mode activated")

        await self.game_init()
        
        game_data = await self.redis.get(f'{self.room_group_name}:game')
        game = Game.from_dict(json.loads(game_data))
        if game.get_state() != 'init':
            return
        game.set_state('load')
        await self.redis.set(f'{self.room_group_name}:game', json.dumps(game.to_dict()))
        
        await self.pads_init(game, 10, 50)
        print('GO')
        asyncio.create_task(self.send_game_state())

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game.update',
            'game': event['game'],
            'padA': event['padA'],
            'padB': event['padB'],
            'ball': event['ball']
        }))

    async def game_init(self):
        game_data = await self.redis.get(f'{self.room_group_name}:game')
        print(f'Game : {game_data}.')

        if not game_data:
            game = Game(
                width=800,
                height=600,
                type='1vs1'     # '1vs1', '2vs2', '4players'
            )
            game.set_user('A', self.user.id)
            await self.redis.set(f'{self.room_group_name}:game', json.dumps(game.to_dict()))
            return

        game = Game.from_dict(json.loads(game_data))
        if game.get_user('A') == self.user.id:  # A modifier pour jouer a 2 sur le meme clavier !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return
        if game.get_user('B'):
            return
        
        game.set_user('B', self.user.id)
        game.set_state('start')
        await self.redis.set(f'{self.room_group_name}:game', json.dumps(game.to_dict()))
        print(f'F Game : {game}.')

    async def pads_init(self, game, width, height):
        x = 10
        y = game.height / 2

        padA = Pad('A', x=width, y=y, h=height, w=width)
        padB = Pad('B', x=game.width - width, y=y, h=height, w=width)

        await self.redis.set(f'{self.room_group_name}:padA', json.dumps(padA.to_dict()))
        await self.redis.set(f'{self.room_group_name}:padB', json.dumps(padB.to_dict()))

        ball = Ball(x = 400, y = 300, r = 5, speed = 5)
        await self.redis.set(f'{self.room_group_name}:ball', json.dumps(ball.to_dict()))

    async def pads_get_players(self):
        game = await self.get_game()
        padA, padB = await self.get_pads()

        padA.set_player_id(game.get_user('A'))
        padB.set_player_id(game.get_user('B'))

    async def send_game_state(self):
        await self.loading()

        while True:
            game = await self.get_game()
            padA, padB = await self.get_pads()
            ball = await self.get_ball()

            ball.update(padA, padB, game.height, game.width)
            update_score(game, padA, padB)
            await self.set_data(game, padA, padB, ball)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game.update',
                    'game': json.dumps(game.to_dict()),
                    'padA': json.dumps(padA.to_dict()),
                    'padB': json.dumps(padB.to_dict()),
                    'ball': json.dumps(ball.to_dict())
                }
            )
            # await asyncio.sleep(1/30)  # Pause pour envoyer à 60 FPS
            await asyncio.sleep(1/60)  # Pause pour envoyer à 60 FPS

    async def set_data(self, game, padA, padB, ball):
        game_data = json.dumps(game.to_dict())
        padA_data = json.dumps(padA.to_dict())
        padB_data = json.dumps(padB.to_dict())
        ball_data = json.dumps(ball.to_dict())

        await self.redis.set(f'{self.room_group_name}:game', game_data)
        await self.redis.set(f'{self.room_group_name}:padA', padA_data)
        await self.redis.set(f'{self.room_group_name}:padB', padB_data)
        await self.redis.set(f'{self.room_group_name}:ball', ball_data)

    async def get_pads(self):
        padA_data = await self.redis.get(f'{self.room_group_name}:padA')
        padB_data = await self.redis.get(f'{self.room_group_name}:padB')
        
        padA = Pad.from_dict(json.loads(padA_data))
        padB = Pad.from_dict(json.loads(padB_data))
            
        if 0:
            print(f'padA data : {padA_data}')
            print(f'padB data : {padB_data}')

        return padA, padB
