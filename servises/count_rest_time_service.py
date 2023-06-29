import time
import datetime


def count_rest_time_service(subscribtion_expire_time: int) -> str:
    '''
    subscribtion_expire_time -> get from user model subscribe time
    calculete rest subscription\'s time in seconds
    and convert it to day/time format
    '''
    expire_time_seconds = subscribtion_expire_time-int(time.time())
    expire_time = str(datetime.timedelta(
        seconds=expire_time_seconds))
    expire_time.replace('days', 'дней')
    expire_time.replace('day', 'день')
    return expire_time
