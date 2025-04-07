import pika
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from .models import CustomUser
from .producer import *
import traceback

RABBITMQ_HOST = 'localhost'


def get_user_details(user_id):
    try:
        if isinstance(user_id, dict) and 'error' in user_id:
            print("User not found, skipping DB call.")
            return None  # or handle it however you need
    # try:
    #     user = CustomUser.objects.get(id=user_id)
    # except CustomUser.DoesNotExist:
    #     print("User not found in DB")
        # return None
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            traceback.print_exc()
            return {"error": "User not found"}
        return {
            "user_id": user.id,
            "name": user.username,
            "email": user.email,
            "mobile_number": user.mobile_number
        }
    except :
        traceback.print_exc()
        return {"error": "User not found"}

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        user_id = data.get("user_id")
            
        print(f"📩 Received request for user_id: {user_id} | correlation_id: {properties.correlation_id}")

        user_details = get_user_details(user_id)
        response_message = json.dumps(user_details)

        ch.queue_declare(queue='user_response_queue', durable=True)
        ch.basic_publish(
            exchange='',
            routing_key='user_response_queue',
            body=response_message,
            properties=pika.BasicProperties(
                delivery_mode=2,
                correlation_id=properties.correlation_id  # echo back same ID
            )
        )

        print(f"✅ Sent user details with correlation_id: {properties.correlation_id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except:
        import traceback
        traceback.print_exc()


def start_consumer(channel):
    # connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    # channel = connection.channel()

    channel.queue_declare(queue='user_request_queue', durable=True)
    channel.basic_consume(queue='user_request_queue', on_message_callback=callback)

    print(" [*] Waiting for messages from product_module...")
    channel.start_consuming()
