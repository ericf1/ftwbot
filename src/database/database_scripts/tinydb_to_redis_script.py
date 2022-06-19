import json
import redis
from redis.commands.json.path import Path
import os


def tinydb_to_redis(dir):

    social_data = redis.Redis(host='localhost', port=6379, db=0)
    time_data = redis.Redis(host='localhost', port=6379, db=1)
    settings_data = redis.Redis(host='localhost', port=6379, db=2)
    channels_data = redis.Redis(host='localhost', port=6379, db=3)

    with open(dir) as json_file:
        data = json.load(json_file)

    for server_id, socials in data.items():
        new_social_data = data[server_id]["1"].get("socials")
        if new_social_data is not None:
            social_data.json().set(server_id, Path.root_path(), new_social_data)
            print(f'Social Data: {social_data.json().get(server_id)}')

        new_time_data = data[server_id]["1"].get("prevTime")
        if new_time_data:
            time_data.set(server_id, new_time_data)
            decoded = time_data.get(server_id).decode('utf-8')
            print(f'Time Data: {decoded}')

        new_settings_data = {"language": "English", "send_video_as_link": "No"}

        settings_data.json().set(server_id, Path.root_path(), new_settings_data)
        print(f'Settings Data: {settings_data.json().get(server_id)}')

        new_channel_data = data[server_id]["1"].get("channelID")
        if new_channel_data is not None:
            channels_data.sadd(server_id, new_channel_data)
            decoded = [member.decode('utf-8')
                       for member in channels_data.smembers(server_id)]
            print(f'Channel Data: {decoded}\n')


# docker run -d -p 6379:6379 -v <volume-name>:/data --name ftw redislabs/rejson:latest
# docker run -d -p 6379:6379 -v <path>:/data --name ftw redislabs/rejson:latest
# To find the volume location you have to use docker volume inspect <volume name>
# docker run -d -p 6379:6379 -v ftw:/data --name ftw redislabs/rejson:latest
if __name__ == "__main__":
    rel_path = "src\database\database_scripts"
    json_files = [file for file in os.listdir(rel_path) if ".json" in file]

    for file in json_files:
        tinydb_to_redis(rel_path + "\\" + file)
