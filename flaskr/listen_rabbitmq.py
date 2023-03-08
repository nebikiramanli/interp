import pika
from flaskr.config import Config
from datetime import datetime
import json
from model.postgresql.notice import Notice


class Consumer:
    def __init__(self, host, queue, port=5672, exchange='', routing_key=''):
        self.host = host
        self.queue = queue
        self.port = port
        self.exchange = exchange
        self.routing_key = routing_key
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
            print("RabbitMQ connection established")

        except Exception as e:
            print("RabbitMQ connection error: ", e)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r " % body)
        print('Message received!' + str(datetime.now()))
        self.save_to_db(body)
        self.save_to_json(body)

    def consume(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def connect_and_consume(self):
        self.connect()
        print("RabbitMQ connection established")
        self.consume()
        print("RabbitMQ consume established")

    def save_to_db(self, message):
        print("Saving message to database...")
        message = message.decode('utf-8')
        message_json = json.loads(message)
        print("Message: ", message)
        notice = Notice()
        conn = notice.connect(host=Config.DB_HOST,
                              port=Config.DB_PORT,
                              database=Config.DB_NAME,
                              user=Config.DB_USER,
                              password=Config.DB_PASSWORD)

        base_model = {
            'entity_id': None,
            'forename': None,
            'date_of_birth': None,
            'nationalities': None,
            'name': None,
            'link_self': None,
            'link_image': None,
            'link_thumbnail': None,
            'created_at': None,
            'updated_at': None,
            'is_deleted': None
        }
        for item in message_json:
            base_model['entity_id'] = item.get('entity_id')
            base_model['forename'] = item.get('forename')
            base_model['date_of_birth'] = item.get('date_of_birth')
            base_model['nationalities'] = '{' + ' '.join(item.get('nationalities')) + '}' if item.get('nationalities') is not None else None
            base_model['name'] = item.get('name')
            links = item.get('_links')
            base_model['link_self'] = links.get('self').get('href') if links.get('self') is not None else None
            base_model['link_image'] = links.get('images').get('href') if links.get('images') is not None else None
            base_model['link_thumbnail'] = links.get('thumbnail').get('href') if links.get('thumbnail') is not None else None
            base_model['created_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            base_model['updated_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            base_model['is_deleted'] = False
            item = (base_model['entity_id'], base_model['forename'], base_model['date_of_birth'], base_model['nationalities'], base_model['name'], base_model['link_self'], base_model['link_image'], base_model['link_thumbnail'], base_model['created_at'], base_model['updated_at'], base_model['is_deleted'])
            notice.insert(conn, item)
        notice.close(conn)
        print("Message saved to database!")

    def save_to_json(self, message):
        print("Saving message to file...")
        message = message.decode('utf-8')
        message_json = json.loads(message)
        print("Message: ", message)
        with open('message.json', 'w') as f:
            f.write(message)
            print("Message saved to file!")

    def close(self):
        self.connection.close()
        print("RabbitMQ connection closed")

    def __del__(self):
        self.close()

'''
if __name__ == '__main__':
    rabbitmq_host = Config.RABBITMQ_HOST
    queue = Config.RABBITMQ_QUEUE
    print(rabbitmq_host, queue)
    consumer = Consumer(rabbitmq_host, queue)
    consumer.connect_and_consume()

'''