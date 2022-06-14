from database.ChannelsDatabase import ChannelsDatabase
from database.SocialDatabase import SocialDatabase
from database.TimeDatabase import TimeDatabase
from database.SettingsDatabase import SettingsDatabase


def export_redis():
    social_database = SocialDatabase(0)
    time_database = TimeDatabase(1)
    settings_database = SettingsDatabase(2)
    channels_database = ChannelsDatabase(3)

    exported_json = dict()

    for social in social_database.all:
        exported_json.update(social)

    for time in time_database.all:
        exported_json.update(time)

    for setting in settings_database.all:
        exported_json.update(setting)

    for channel in channels_database.all:
        exported_json.update(channel)

    print(exported_json)


if __name__ == "__main__":
    export_redis()
