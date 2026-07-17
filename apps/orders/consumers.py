import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_number = self.scope['url_route']['kwargs']['order_number']
        self.room_group_name = f'order_track_{self.order_number}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send initial status acknowledgment
        await self.send(text_data=json.dumps({
            'status': 'connected',
            'message': f'Live tracking established for #{self.order_number}'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        # Broadcast update to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'order_status_update',
                'status': data.get('status', 'processing'),
                'message': message
            }
        )

    async def order_status_update(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status'],
            'message': event['message']
        }))
