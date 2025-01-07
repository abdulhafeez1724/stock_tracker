import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import fetch_stock_data  # Ensure this is an async task

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("stock_updates", self.channel_name)
        await self.accept()

        # Fetch initial data
        await self.send_stock_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("stock_updates", self.channel_name)

    async def send_stock_data(self):
        stock_data = await fetch_stock_data()  # This should be awaited
        await self.send(text_data=json.dumps(stock_data))

    async def stock_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
