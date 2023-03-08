import pika
import json


def send_message(host, queue, message, port=5672, exchange='', routing_key='interpol'):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        message = json.dumps(message).encode('utf-8')
        print("Message: ", message)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        print("Message sent!")
        connection.close()

    except Exception as e:
        print("RabbitMQ connection error: ", e)