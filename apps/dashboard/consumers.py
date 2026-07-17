import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardTelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'admin_dashboard_telemetry'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            'status': 'connected',
            'revenue': '1842600.00',
            'orders': 148,
            'message': 'Executive telemetry stream active.'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'telemetry_update',
                'revenue': data.get('revenue', '1842600.00'),
                'orders': data.get('orders', 148)
            }
        )

    async def telemetry_update(self, event):
        await self.send(text_data=json.dumps({
            'revenue': event['revenue'],
            'orders': event['orders']
        }))
