import os
from dotenv import load_dotenv
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load Environment Variables
load_dotenv(os.path.join(main_project_dir, '.env'))


class Config:
    # RabbitMQ Environment Variables
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
    RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY')

    # Data Source Environment Variables

    # Database Environment Variables
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')



