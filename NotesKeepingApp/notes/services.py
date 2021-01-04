import logging
import redis

r = redis.StrictRedis()


class Cache(object):

    # def __init__(self):
    #     self.r = redis.StrictRedis(host='http://127.0.0.1:8000/', port=6379)

    @staticmethod
    def set_cache(key, val):
        r.set(key, val)
        r.expire(key, time = 100)
    @staticmethod
    def get_cache( key):
        id = r.get(key)
        return id
    @staticmethod
    def clear_cache():
        r.flushall()
        logging.debug("Cache Flushed")
