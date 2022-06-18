# modals
# social_data -> server_id: {twitter: [usernames], instagram: [usernames], ...}
# time_data -> server_id: timestamp
# channels_data -> server_id: [channels]
# settings_data -> server_id: {{"language":language, "video_as_link":video_as_link}}


class Database:
    __slots__ = ("data")

    def __init__(self, db_val):
        pass

    def __repr__(self):
        pass

    @property
    def all(self):
        pass

    @property
    def db(self):
        pass

    def get(self, server_id):
        pass

    def add(self, server_id, *args, **kwargs):
        pass

    def remove(self, server_id, *args, **kwargs):
        pass
