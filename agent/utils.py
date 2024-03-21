import redis as redis
import json

import logging
import logging.handlers

LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']

def check_notify(r):
    r.config_set('notify-keyspace-events', 'KEA')
    pass

def get_logger(level='DEBUG', file_name=None):
    if file_name == None:
        print(f'Should always assign the name for the logger.')
        raise Exception
    elif not level.upper() in LOG_LEVELS:
        print(f'Set an invalid log level, {level.upper()}')
        raise Exception
    else:
        if file_name.find('.log'):
            LOG_DIRECTORY = '/var/log/' + file_name
        else:
            LOG_DIRECTORY = '/var/log/' + file_name + '.log'
        formatter = '[%(asctime)s] [%(levelname)s] %(message)s'
        logging.basicConfig(level=level.upper(), filename=LOG_DIRECTORY, format=formatter)
        logger = logging.getLogger()
        return logger


def redis_setup(db_host='localhost', db_port=6379, db_ch='channel_1', db_idx=0, sub_pattern='Test'):
    r = redis.Redis(host=db_host, port=db_port, db=db_idx)

    # subprefix = f'__keyevent@{db_idx}__:*'
    subprefix = f'__keyspace@{db_idx}__:{sub_pattern}:*'

    if r.config_get('notify-keyspace-events') != 'KEA':
        # print("set notify-keyspace-events to KEA")
        check_notify(r)
    return r, subprefix
    pass

def utf8_decode(msg):
    return msg.decode("utf-8")

def utf8_len(msg):
    try:
        msg = utf8_decode(msg)
    except:
        pass
    return len(msg)