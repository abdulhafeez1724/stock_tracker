import json
import requests
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings


@shared_task
async def fetch_stock_data():
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey={settings.ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    stock_data = {
        'symbol': data['Global Quote']['01. symbol'],
        'price': data['Global Quote']['05. price'],
        'change_percent': data['Global Quote']['10. change percent'],
    }
    
    # Send the data to the group
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        "stock_updates",
        {
            "type": "stock_update",
            "data": stock_data,
        }
    )
    
    return stock_data
