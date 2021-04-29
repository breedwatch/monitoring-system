import datetime
import os
import pytz


def get_time(is_dataset=False):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if not is_dataset:
        return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0]
    else:
        return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0] + 'Z'


def get_diff_seconds(last_time):
    now = get_token_time()
    if last_time != "":
        diff = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S') \
               - datetime.datetime.strptime(last_time, '%Y-%m-%dT%H:%M:%S')
        return float(diff.total_seconds())
    else:
        return False


def get_new_date(estimated_hours):
    current_date_and_time = datetime.datetime.now()
    hours_added = datetime.timedelta(hours=estimated_hours)
    future_date_and_time = current_date_and_time + hours_added
    return future_date_and_time.strftime('%Y-%m-%dT%H:%M:%S')


def get_token_time():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0]


def get_file_time():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).now()
    return now.strftime('%Y-%m-%dT%H-%M-%S') + now.strftime('.%f')[:0]


def get_dir_time():
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).now()
    return now.strftime('%Y-%m-%d')


def set_timezone(timezone):
    try:
        new_timezone = 'sudo timedatectl set-timezone {}'.format(timezone)
        os.system(new_timezone)
    except Exception as e:
        print(e)
