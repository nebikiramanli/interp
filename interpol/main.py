import notice
import producer
from config import Config
import scheduler


def main():
    rabbitmq_host = Config.RABBITMQ_HOST
    rabbitmq_port = Config.RABBITMQ_PORT
    rabbitmq_queue = Config.RABBITMQ_QUEUE
    rabbitmq_routing_key = Config.RABBITMQ_ROUTING_KEY
    base_url = Config.BASE_URL
    notice_url = Config.NOTICE_URL
    notice_type = Config.NOTICE_TYPE
    notice_version = Config.NOTICE_VERSION

    url = base_url + notice_url + notice_version + notice_type
    data = notice.get_all_notices(url)
    print(data)
    producer.send_message(host=rabbitmq_host, port=rabbitmq_port, queue=rabbitmq_queue,
                          routing_key=rabbitmq_routing_key, message=data)


if __name__ == '__main__':
    _scheduler_period = int(Config.SCHEDULER_PERIOD)
    _scheduler_type = Config.SCHEDULER_TYPE
    sleep_time = int(Config.SLEEP_TIME)
    scheduler.scheduler_period(period=_scheduler_period, period_type=_scheduler_type, func=main)
    scheduler.run_scheduler(sleep_time=sleep_time)

