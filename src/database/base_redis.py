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
    def all(self):
        def all_items(db):
            return [key for key in db.scan_iter("user:*")]
        return all_items(self.social_data)


if __name__ == "__main__":
    socials_database = SocialsDatabase()
    print(socials_database.all)
