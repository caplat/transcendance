import json

from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import User42
from asgiref.sync import sync_to_async
from .models import PrivateMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()  # Close the connection if the user is not authenticated
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')

        user = self.scope['user']
        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'User not authenticated'
            }))
            return

        print(f"Received message: {message} from user: {username}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))


        # Exemple d'utilisation de self.scope['user']
class PrivateChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None

    async def connect(self):
        # Récupère l'utilisateur connecté à partir de la session
        self.user = self.scope['user']

        # Vérifie si l'utilisateur est authentifié
        if not self.user.is_authenticated:
            await self.close()
            return

        # Utilise l'ID de l'utilisateur connecté pour créer un groupe privé
        self.room_group_name = f"private_chat_{self.user.id}"

        # Rejoindre le groupe de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de chat
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Recevoir un message du WebSocket
    async def receive(self, text_data):
        # Check if the user is still authenticated
        if not self.user.is_authenticated:
            await self.send(text_data=json.dumps({'error': 'User not authenticated'}))
            return  # Exit early if user is not authenticated

        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        recipient_username = text_data_json.get('recipient')

        if not message or not recipient_username:
            await self.send(text_data=json.dumps({'error': 'Message and recipient are required'}))
            return

        try:
            # Retrieve the recipient user from the database
            recipient = await sync_to_async(User42.objects.get)(username=recipient_username)
        except User42.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Recipient does not exist'}))
            return

        # Save the private message to the database
        private_message = PrivateMessage(sender=self.user, recipient=recipient, message=message)
        await sync_to_async(private_message.save)()

        # Prepare to send the message to the recipient's group
        recipient_group_name = f"private_chat_{recipient.id}"
        await self.channel_layer.group_send(
            recipient_group_name,
            {
                'type': 'private_chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )
    # Recevoir le message du groupe
    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))