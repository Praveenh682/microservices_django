import pika
import json

RABBITMQ_HOST = 'localhost'

def publish_message(user_id):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue='user_response_queue',durable=True)

        message = json.dumps({"user_id":user_id})
        print('yesss',message)
        channel.basic_publish(
            exchange='',
            routing_key='user_request_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        connection.close()

    except:
        import traceback
        traceback.print_exc()