from .Database import Database
import redis
import time


class TimeDatabase(Database):
    __slots__ = ("data")

    def __init__(self, db_val):
        self.data = redis.Redis(host='localhost', port=6379, db=db_val)

    def __repr__(self):
        return str(self.all())

    @property
    def all(self):
        return [{key.decode('utf-8'): self.data.get(key.decode('utf-8')).decode('utf-8')} for key in self.data.scan_iter()]

    @property
    def db(self):
        return self.data

    def check(self, server_id: str):
        all_keys = [key.decode('utf-8') for key in self.data.scan_iter()]
        if not server_id in all_keys:
            self.data.set(server_id, int(time.time()))

    def get(self, server_id):
        self.check(server_id)
        return int(float(self.data.get(server_id).decode('utf-8')))

    def add(self, server_id, new_time: int):
        self.check(server_id)
        self.data.set(server_id, new_time)

    def remove(self, server_id, *args, **kargs):
        pass
