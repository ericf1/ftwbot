import redis
import sys

social_data = redis.Redis(host='localhost', port=6379, db=0)
time_data = redis.Redis(host='localhost', port=6379, db=1)
settings_data = redis.Redis(host='localhost', port=6379, db=2)

if sys.argv is None:
    for key in social_data.scan_iter():
        pass
