from .Database import Database
import redis
from redis.commands.json.path import Path
from ._supported_settings import SUPPORTED_SETTINGS_DATA, DEFAULT_SETTINGS_DATA


class SettingsDatabase(Database):
    __slots__ = ("data")

    def __init__(self, db_val):
        self.data = redis.Redis(host='localhost', port=6379, db=db_val)

    def __repr__(self):
        # return {{key.decode('utf-8'): self.data.json().get(key.decode('utf-8'))} for key in self.social_data.scan_iter()}
        return str(self.all())

    @property
    def all(self):
        return [{key.decode('utf-8'): self.data.json().get(key.decode('utf-8'))} for key in self.data.scan_iter()]

    @property
    def db(self):
        return self.data

    def get(self, server_id):
        self.check(server_id)
        return self.data.json().get(server_id)
    
    def check(self, server_id: str):
        all_keys = [key.decode('utf-8') for key in self.data.scan_iter()]
        if not server_id in all_keys:
            self.data.json().set(server_id, Path.root_path(), DEFAULT_SETTINGS_DATA)

    # This is more like "update"
    def add(self, server_id, **kwargs):
        self.check(server_id)
        original_data = self.get(server_id)
        for key, value in kwargs.items():
            if key in SUPPORTED_SETTINGS_DATA and value in SUPPORTED_SETTINGS_DATA[key]:
                original_data[key] = value
            else:
                raise KeyError("Unsupported setting")
        self.data.json().set(server_id, Path.root_path(), original_data)

    def remove(self, server_id, *args, **kwargs):
        pass
