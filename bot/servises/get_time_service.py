__all__=['get_time']


from datetime import datetime

def get_time():
    time = datetime.today().strftime('%Y-%m-%d').replace('-', '/')
    return time