import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat."""

    async def connect(self):
        """Handle WebSocket connection."""
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle messages received from WebSocket."""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'typing':
            await self.handle_typing(data)
        elif message_type == 'read_receipt':
            await self.handle_read_receipt(data)

    async def handle_chat_message(self, data):
        """Handle sending a chat message."""
        message_content = data.get('message', '')

        # Save message to database
        message = await self.save_message(
            conversation_id=self.conversation_id,
            sender=self.user,
            content=message_content
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message_handler',
                'message': {
                    'id': str(message.id),
                    'sender': {
                        'id': str(message.sender.id),
                        'username': message.sender.username,
                        'avatar': message.sender.avatar.url if message.sender.avatar else None,
                    },
                    'content': message.content,
                    'created_at': message.created_at.isoformat(),
                }
            }
        )

    async def handle_typing(self, data):
        """Handle typing indicator."""
        is_typing = data.get('is_typing', False)

        # Broadcast typing status to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_handler',
                'user_id': str(self.user.id),
                'username': self.user.username,
                'is_typing': is_typing,
            }
        )

    async def handle_read_receipt(self, data):
        """Handle message read receipt."""
        message_id = data.get('message_id')

        # Mark message as read
        await self.mark_message_as_read(message_id, self.user)

        # Broadcast read receipt to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'read_receipt_handler',
                'message_id': message_id,
                'user_id': str(self.user.id),
                'username': self.user.username,
            }
        )

    async def chat_message_handler(self, event):
        """Send chat message to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': event['message']
        }))

    async def typing_handler(self, event):
        """Send typing indicator to WebSocket."""
        # Don't send typing indicator back to sender
        if str(self.user.id) != event['user_id']:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'user_id': event['user_id'],
                'username': event['username'],
                'is_typing': event['is_typing'],
            }))

    async def read_receipt_handler(self, event):
        """Send read receipt to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id'],
            'user_id': event['user_id'],
            'username': event['username'],
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, sender, content):
        """Save message to database."""
        from chat.models import Conversation, Message
        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )
        return message

    @database_sync_to_async
    def mark_message_as_read(self, message_id, user):
        """Mark message as read in database."""
        from chat.models import Message, MessageReadReceipt
        try:
            message = Message.objects.get(id=message_id)
            MessageReadReceipt.objects.get_or_create(
                message=message,
                user=user
            )
        except Message.DoesNotExist:
            pass


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications."""

    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.room_group_name = f'notifications_{self.user.id}'

        # Join notification group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave notification group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle messages received from WebSocket."""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'mark_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_read(notification_id)

    async def notification_handler(self, event):
        """Send notification to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'data': event['notification']
        }))

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read in database."""
        from notifications.models import Notification
        try:
            notification = Notification.objects.get(id=notification_id, recipient=self.user)
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass
