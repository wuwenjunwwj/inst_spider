import redis
import logging
class redis_handler(object):
    def __init__(self, host='localhost', port=6379, db=None):
        self.host = host
        self.port = port
        self.db = db
        pass
    def write(self, key, value):
        try:
            self.r.set(key, value)
        except redis.exceptions.RedisError, e:
            print e
    def read(self, key):
        try:
            value = self.r.get(key)
            return value
        except redis.exceptions.RedisError, e:
            print e
    def connect_db(self):
        self.r = redis.Redis(self.host, self.port, self.db)

class redis_client(object):
    def __init__(self, host, port, db):
        self.redis_handler = redis_handler('localhost', 6379, 0)
        self.redis_handler.connect_db()
        #redis_handler.write('key-wwj', 'value-wwj')
        #value = redis_handler.read('key-wwj')
    def get_data(self):
        pass
    def start(self):
        
        pass
