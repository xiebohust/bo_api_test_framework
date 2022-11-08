import datetime
import shutil
import time,re
import config
import requests
from utils.redis_handle import RedisHandle



def current_time():
    return time.strftime('%Y%m%d%H%M%S')




def today():
    return time.strftime('%Y%m%d')


def get_user_session(pattern='user_session_(\w+)'):
    keys = RedisHandle().keys()
    for key in keys:
        result = re.findall(pattern, key)
        if result:
            print(result)
            return result[0]
    return None

def rm_dir():
    shutil.rmtree('aaa/',ignore_errors=True)

if __name__ == '__main__':
    # get_user_session()
    rm_dir()