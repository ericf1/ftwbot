from database.ChannelsDatabase import ChannelsDatabase
from database.SocialDatabase import SocialDatabase
from database.TimeDatabase import TimeDatabase
from database.SettingsDatabase import SettingsDatabase
import json


def export_redis():
    social_database = SocialDatabase(0)
    time_database = TimeDatabase(1)
    settings_database = SettingsDatabase(2)
    channels_database = ChannelsDatabase(3)

    exported_json = dict()

    for social in social_database.all:
        for key, value in social.items():
            if exported_json.get(key) is None:
                exported_json[key] = {}
            exported_json[key].update({"socials": value})

    for time in time_database.all:
        for key, value in time.items():
            if exported_json.get(key) is None:
                exported_json[key] = {}
            exported_json[key].update({"prev_time": value})

    for setting in settings_database.all:
        for key, value in setting.items():
            if exported_json.get(key) is None:
                exported_json[key] = {}
            exported_json[key].update({"settings": value})

    for channel in channels_database.all:
        for key, value in channel.items():
            if exported_json.get(key) is None:
                exported_json[key] = {}
            exported_json[key].update({"channel_ids": value})

    dumped_json = json.dumps(exported_json, indent=4)
    with open("new_database.json", "w") as outfile:
        outfile.write(dumped_json)


if __name__ == "__main__":
    export_redis()
