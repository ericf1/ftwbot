import json
import redis
from redis.commands.json.path import Path

social_data = redis.Redis(host='localhost', port=6379, db=0)
time_data = redis.Redis(host='localhost', port=6379, db=1)

with open('redis-scripts\database.json') as json_file:
    data = json.load(json_file)

corrected_key_value_pairs = {}
time_key_value_pairs = {}
for server_id, socials in data.items():
    time_value = data[server_id]["1"]["prevTime"]
    del data[server_id]["1"]["prevTime"]
    # corrected_key_value_pairs[server_id] = data[server_id]["1"]
    time_data.set(server_id, time_value)
    social_data.json().set(server_id, Path.root_path(), data[server_id]["1"])

# with open('redis-data.json', 'w') as f:
    # json.dump(corrected_key_value_pairs, f)

# docker run -d -p 6379:6379 -v <volume-name>:/data --name ftw redislabs/rejson:latest
# docker run -d -p 6379:6379 -v <path>:/data --name ftw redislabs/rejson:latest
# To find the volume location you have to use docker volume inspect <volume name>

# docker run -d -p 6379:6379 -v ftw:/data --name ftw redislabs/rejson:latest
