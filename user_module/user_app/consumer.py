import pika
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from functions import get_user_details

RABBITMQ_HOST = 'localhost'

def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data.get("user_id")

    user_details = get_user_details(user_id)

    response_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    response_channel = response_connection.channel()

    response_channel.queue_declare(queue='user_response_queue', durable=True)
    response_message = json.dumps(user_details, cls=DjangoJSONEncoder)

    response_channel.basic_publish(
        exchange='',
        routing_key='user_response_queue',
        body=response_message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )

    print(f" [✔] Sent user details for {user_id}")
    response_connection.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='user_request_queue', durable=True)
    channel.basic_consume(queue='user_request_queue', on_message_callback=callback)

    print(" [*] Waiting for messages from product_module...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
