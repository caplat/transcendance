import json
import uuid
import asyncio
import redis.asyncio as aioredis

from channels.generic.websocket import AsyncWebsocketConsumer

from .Game import Game
from .Pad import Pad
from .Ball import Ball


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.redis = await aioredis.from_url('redis://redis:6379/0', decode_responses=True)
        self.game_type = self.scope['url_route']['kwargs']['game_type']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'game_{self.game_type}_{self.room_id}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print('DISCONNECT')
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # gerer les probleme de deconnection et metre la partie en pause
        
        game_data = await self.redis.get(f'{self.room_group_name}:game')
        game = Game.from_dict(json.loads(game_data))
        
        if self.user.id in game.users:
            print(f'USER {self.user.id} DISCONNECT')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game.disconnect',
                    'user': self.user.id
                }
            )
        self.redis.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print('RECEIVE DATA : ', text_data_json)
        
        dir = text_data_json.get('pad', '')

        if text_data_json['type'] == 'game.updatePad':
            await self.update_pad(text_data_json)
        elif text_data_json['type'] == 'game.play':
            await self.play()

    async def game_loading(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game.loading',
            'game': event['game']
        }))

    async def game_ready(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game.ready',
            'game': event['game']
        }))

    async def game_disconnect(self, event):
        print('EVENT : ', event)
        await self.send(text_data=json.dumps({
            'type': 'game.disconnect',
            'user': event['user']
        }))

    async def loading(self):
        game_data = await self.redis.get(f'{self.room_group_name}:game')
        game = Game.from_dict(json.loads(game_data))

        while game.get_state() != 'start':
            game_data = await self.redis.get(f'{self.room_group_name}:game')
            game = Game.from_dict(json.loads(game_data))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game.loading',
                    'game': json.dumps(game.to_dict())
                }
            )
            await asyncio.sleep(1/30)

        await self.pads_get_players()

        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    'type': 'game.ready',
                    'game': json.dumps(game.to_dict())
                }
            )
        
    async def play(self):
        ball_data = await self.redis.get(f'{self.room_group_name}:ball')
        ball = Ball.from_dict(json.loads(ball_data))
        
        ball.start()
        await self.redis.set(f'{self.room_group_name}:ball', json.dumps(ball.to_dict()))

    async def update_pad(self, text_data_json):
        pad_id = text_data_json.get('pad', '')
        pad_name = f'{self.room_group_name}:pad' + pad_id
        dir = text_data_json.get('dir', '')
        vy = text_data_json.get('vy', '')

        pad_data = await self.redis.get(pad_name)
        pad = Pad.from_dict(json.loads(pad_data))
        pad.update(dir, vy)
        await self.redis.set(pad_name, json.dumps(pad.to_dict()))

    async def get_game(self):
        game_data = await self.redis.get(f'{self.room_group_name}:game')
        game = Game.from_dict(json.loads(game_data))

        if 0:
            print(f'game data : {game_data}')

        return game

    async def get_ball(self):
        ball_data = await self.redis.get(f'{self.room_group_name}:ball')
        
        ball = Ball.from_dict(json.loads(ball_data))

        if 0:
            print(f'ball data : {ball_data}')

        return ball
