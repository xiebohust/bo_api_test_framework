import redis
import config

class RedisHandle:

    def __init__(self,host=config.REDIS_HOST,port=config.REDIS_PORT,password=config.REDIS_PASSWORD):
        self.conn = redis.Redis(host=host,port=port,password=password,db=3,decode_responses=True)

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value):
        return self.conn.set(key,value)

    def keys(self):
        return self.conn.keys()

    def remove(self,key):
        return self.conn.delete(key)
    def __del__(self):
        return self.conn.close()

if __name__ == '__main__':
    key = ''

    # import re
    # rs = re.findall('user_session_(\w+)',key)
    # if rs:
    #     print(rs)
    r = RedisHandle()
    s = r.get(key)
    print(s)
    print(r.remove(key))
