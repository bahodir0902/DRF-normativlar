import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{self.user.pk}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            "superusers",
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": f"Connected as {self.user.email}"
        }))

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        if hasattr(self, 'user') and self.user.is_superuser:
            await self.channel_layer.group_discard(
                "superusers",
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        pass #biz xabarlarni qabul qilmaymiz, faqat koramiz

    async def notification_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event['message']
        }))