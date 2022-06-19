from .Database import Database
import redis
from redis.commands.json.path import Path


class SocialDatabase(Database):
    __slots__ = ("data")

    def __init__(self, db_val):
        self.data = redis.Redis(host='localhost', port=6379, db=db_val)

    def __repr__(self):
        return str(self.all())

    @property
    def all(self):
        return [{key.decode('utf-8'): self.data.json().get(key.decode('utf-8'))} for key in self.data.scan_iter()]

    @property
    def db(self):
        return self.data

    def check(self, server_id: str):
        all_keys = [key.decode('utf-8') for key in self.data.scan_iter()]
        if not server_id in all_keys:
            self.data.json().set(server_id, Path.root_path(), {})

    def get(self, server_id: int):
        server_id = str(server_id)
        self.check(server_id)
        return self.data.json().get(server_id)

    def add(self, server_id: int, social_media, username):
        server_id = str(server_id)
        self.check(server_id)
        original_data = self.data.json().get(server_id)
        if social_media not in original_data:
            original_data[social_media] = []
        if username in original_data[social_media]:
            raise ValueError("User is already in database")
        original_data[social_media].append(username)
        self.data.json().set(server_id, Path.root_path(), original_data)

    def remove(self, server_id: int, social_media, username):
        server_id = str(server_id)
        original_data = self.data.json().get(server_id)
        if original_data is None:
            raise KeyError("No such server exists")
        if original_data.get(social_media) is None:
            raise KeyError("No such social media exists")
        if not username in original_data[social_media]:
            raise KeyError("No such username exists")
        original_data[social_media].remove(username)
        self.data.json().set(server_id, Path.root_path(), original_data)
