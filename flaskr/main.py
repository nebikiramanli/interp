from flaskr.config import Config
from flaskr import listen_rabbitmq

RABBITMQ_HOST = Config.RABBITMQ_HOST
RABBITMQ_PORT = Config.RABBITMQ_PORT
RABBITMQ_QUEUE = Config.RABBITMQ_QUEUE
RABBITMQ_ROUTING_KEY = Config.RABBITMQ_ROUTING_KEY


def rabbitmq(host, port, queue, routing_key):
    """
    This function is used to connect to RabbitMQ and consume messages

    :param host:
    :param port:
    :param queue:
    :return:
    """

    consumer = listen_rabbitmq.Consumer(host=host, port=port, queue=queue, routing_key=routing_key)
    consumer.connect_and_consume()


if __name__ == '__main__':
    rabbitmq(host=RABBITMQ_HOST, port=RABBITMQ_PORT, queue=RABBITMQ_QUEUE, routing_key=RABBITMQ_ROUTING_KEY)
