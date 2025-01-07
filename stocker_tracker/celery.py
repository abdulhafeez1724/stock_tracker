import os
from celery import Celery
from celery.schedules import crontab
from stock.tasks import fetch_stock_data  # Import the fetch_stock_data task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocker_tracker.settings')

app = Celery('stocker_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls fetch_stock_data every 10 seconds
    sender.add_periodic_task(10.0, fetch_stock_data.s(), name='fetch stock data every 10 seconds')
