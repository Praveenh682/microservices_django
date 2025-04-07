import pika
import json

RABBITMQ_HOST = 'localhost'

import pika
import json
from queue import Queue

response_queue = Queue()  

def callback(ch, method, properties, body):
    user_data = json.loads(body)
    print(f" [✔] Received user data: {user_data}")

    response_queue.put(user_data)  
    ch.basic_ack(delivery_tag=method.delivery_tag)
    ch.stop_consuming()

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='user_response_queue', durable=True)
    channel.basic_consume(queue='user_response_queue', on_message_callback=callback)

    print(" [*] Waiting for user details...")
    channel.start_consuming()

    user_data = response_queue.get()
    return user_data
