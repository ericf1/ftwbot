import redis
from redis.commands.json.path import Path

# settings -> server_id: {{"language":language, "video_as_link":video_as_link}}


class SocialsDatabase:
    def __init__(self):
        self.social_data = redis.Redis(host='localhost', port=6379, db=0)
        self.time_data = redis.Redis(host='localhost', port=6379, db=1)
        self.settings_data = redis.Redis(host='localhost', port=6379, db=2)

    def get_socials(self, server_id):
        return self.social_data.json().get(server_id).get("socials")

    def get_time(self, server_id):
        return self.time_data.get(server_id).decode('utf-8')

    def get_channels(self, server_id):
        return self.social_data.json().get(server_id).get("channelIDs")

    def add(self, platform, username, server_id):
        pass

    def remove(self, platform, username, server_id):
        pass

    @property
    def all_socials(self):
        return [{key.decode('utf-8'): self.social_data.json().get(key.decode('utf-8'))} for key in self.social_data.scan_iter()]

    @property
    def all_settings(self):
        return [{key.decode('utf-8'): self.settings_data.get(key.decode('utf-8'))} for key in self.social_data.scan_iter()]

    @property
    def all_time(self):
        return [{key.decode('utf-8'): self.time_data.get(key.decode('utf-8'))} for key in self.social_data.scan_iter()]

    def __repr__(self):
        return f"Social Database: {self.all_socials}\nTime Database: {self.all_time}\nSettings Database: {self.all_settings}"


if __name__ == "__main__":
    socials_database = SocialsDatabase()
    print(socials_database)
