import pika
import json
import uuid

RABBITMQ_HOST = 'localhost'

def publish_message(user_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    correlation_id = str(uuid.uuid4())  # generate unique ID

    message = json.dumps({"user_id": user_id})
    print('📤 Sending request with correlation_id:', correlation_id)

    channel.basic_publish(
        exchange='',
        routing_key='user_request_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
            correlation_id=correlation_id,
            reply_to='user_response_queue'  # not necessary but good practice
        )
    )

    connection.close()
    return correlation_id
