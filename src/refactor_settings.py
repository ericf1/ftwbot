from database.SettingsDatabase import SettingsDatabase
from redis.commands.json.path import Path
from data import DEFAULT_SETTINGS_DATA, SUPPORTED_SETTINGS_DATA

if __name__ == "__main__":
    settings_database = SettingsDatabase(2)
    for server in settings_database.all:
        for id, setting in server.items():
            settings_database.db.json().set(id, Path.root_path(), DEFAULT_SETTINGS_DATA)

    for server in settings_database.all:
        for id, setting in server.items():
            print(id, setting)
