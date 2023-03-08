import os
from dotenv import load_dotenv
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load Environment Variables
load_dotenv(os.path.join(main_project_dir, '.env'))

# Load Environment Variables
load_dotenv()


class Config:
    # RabbitMQ Environment Variables
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
    RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY')

    # Data Source Environment Variables
    BASE_URL = os.getenv('BASE_URL')
    NOTICE_URL = os.getenv('NOTICE_URL')
    NOTICE_TYPE = os.getenv('NOTICE_TYPE')
    NOTICE_VERSION = os.getenv('NOTICE_VERSION')

    # Scheduler Environment Variables
    SCHEDULER_PERIOD = os.getenv('SCHEDULER_PERIOD')
    SCHEDULER_TYPE = os.getenv('SCHEDULER_TYPE')
    SLEEP_TIME = os.getenv('SLEEP_TIME')

