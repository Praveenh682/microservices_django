import pika
import json
from queue import Queue

RABBITMQ_HOST = 'localhost'

response_queue = Queue()
expected_correlation_id = None

def set_expected_correlation_id(corr_id):
    global expected_correlation_id
    expected_correlation_id = corr_id

def callback(ch, method, properties, body):
    global expected_correlation_id
    user_data = json.loads(body)

    # Only accept the response if correlation_id matches
    if properties.correlation_id == expected_correlation_id:
        print(f"✔ Received matched user data: {user_data}")
        response_queue.put(user_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()
    else:
        print("❌ Correlation ID mismatch, discarding.")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='user_response_queue', durable=True)
    channel.basic_consume(queue='user_response_queue', on_message_callback=callback)

    print("📥 Waiting for user details...")
    channel.start_consuming()

    return response_queue.get()
