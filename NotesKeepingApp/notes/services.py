import logging
import redis




class Cache(object):

    def __init__(self):
        self.r = redis.StrictRedis()
    
    def set_cache(self, key, val):
        self.r.set(key, val)
        self.r.expire(key, time = 100)

    def get_cache(self, key):
        id = self.r.get(key)
        return id

    def clear_cache(self):
        self.r.flushall()
        logging.debug("Cache Flushed")

    def delete_cache(self, key):
        """
        @param key: The key of the respective note
        @type key: String
        """
        self.r.delete(key)
