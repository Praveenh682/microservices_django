import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_project.settings')
django.setup()

import pika
from .consumer import start_consumer
import threading


class RabbitMQConnection:
    print(True)
    _instance = None  # Stores the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQConnection, cls).__new__(cls)
            cls._instance.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        return cls._instance

    def get_channel(self):
        return self.connection.channel()

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
# utfyuuioop

rabbitmq = RabbitMQConnection()    
channel1 = rabbitmq.get_channel()
channel2 = rabbitmq.get_channel()

threading.Thread(target=start_consumer, args=(channel1,)).start()
