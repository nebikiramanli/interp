import schedule
import time


def job():
    print("I'm working...")


def scheduler_period(period, period_type: str, func):
    """
    This function is used to schedule a job to run periodically or at a specific time.
    :param period: period of time to run the job
    :param period_type: type of period (seconds, minutes, hours, days)
    :param func: function to run

    :return: None
    """
    if period_type == 'seconds':
        schedule.every(period).seconds.do(func)
    elif period_type == 'minutes':
        schedule.every(period).minutes.do(func)
    elif period_type == 'hours':
        schedule.every(period).hours.do(func)
    elif period_type == 'days':
        schedule.every(period).days.do(func)
    else:
        print('Invalid period type')
        return


def run_scheduler(sleep_time=1):
    """
    This function is used to run the scheduler
    :return: None
    """
    while True:
        schedule.run_pending()
        time.sleep(sleep_time)


if __name__ == '__main__':

    scheduler_period(1, 'seconds', job)
    run_scheduler()
