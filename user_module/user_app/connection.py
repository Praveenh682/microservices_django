import os
import sys
import django

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ✅ Absolute path to the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_project.settings')

django.setup()



import pika
from .consumer import start_consumer
import threading


class RabbitMQConnection:
    """Singleton class to manage RabbitMQ connection & channel per microservice."""
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


# Initialize the connection
rabbitmq = RabbitMQConnection()    
channel1 = rabbitmq.get_channel()
channel2 = rabbitmq.get_channel()

# ✅ Fix threading call: don't use `start_consumer()` directly
threading.Thread(target=start_consumer, args=(channel1,)).start()
