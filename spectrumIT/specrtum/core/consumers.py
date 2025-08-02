import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from core.models.chat_models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        # Проверяем авторизацию
        if self.user == AnonymousUser():
            await self.close()
            return

        # Проверяем доступ пользователя к комнате
        if not await self.check_room_access():
            await self.close()
            return

        # Присоединяемся к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_initial_messages()

    async def disconnect(self, close_code):
        # Покидаем группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Сохраняем сообщение в БД
        await self.save_message(message)

        # Отправляем сообщение в группу комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': str(self.get_current_timestamp()),
                'is_history': False
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    async def send_initial_messages(self):
        """Sending N last messages after connection"""

        messages = await self.get_recent_messages()

        for message in messages:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': message['message'],
                'sender': message['sender'],
                'timestamp': message['timestamp'],
                'is_history': True
            }))

    @database_sync_to_async
    def get_recent_messages(self, limit=50):
        """Getting last messages from DB"""

        room = ChatRoom.objects.get(id=self.chat_id)
        messages = Message.objects.filter(room=room).select_related('sender').order_by('-timestamp')[:limit]

        return [{
            'message': msg.content,
            'sender': msg.sender.username,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]

    @database_sync_to_async
    def check_room_access(self):
        return ChatRoom.objects.filter(
            id=self.chat_id,
            participants__in=[self.user]
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        room = ChatRoom.objects.get(id=self.chat_id)
        Message.objects.create(
            room=room,
            sender=self.user,
            content=content
        )

    def get_current_timestamp(self):
        from django.utils import timezone
        return timezone.now()
    