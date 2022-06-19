from .Database import Database
import redis


class ChannelsDatabase(Database):
    __slots__ = ("data")
    
    def __init__(self, db_id):
        self.data = redis.Redis(host='localhost', port=6379, db=db_id)

    def __repr__(self):
        return self.all()

    @property
    def all(self):
        all_list = []
        for key in self.data.scan_iter():
            member_list = []
            for member in self.data.smembers(key.decode('utf-8')):
                member_list.append(member.decode('utf-8'))
            all_list.append({key.decode('utf-8'): member_list})
        return all_list

    @property
    def db(self):
        return self.data

    def get(self, server_id):
        try:
            return [member.decode('utf-8') for member in self.data.smembers(server_id)]
        except Exception as e:
            print(repr(e))
            return []

    def add(self, server_id, channel_id):
        self.data.sadd(server_id, channel_id)

    def remove(self, server_id, channel_id):
        self.data.srem(server_id, channel_id)
