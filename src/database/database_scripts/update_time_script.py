# updates all timestamps and tests the json file's structure
import time
import redis
import time


def main():
    time_data = redis.Redis(host='localhost', port=6379, db=1)
    for key in time_data.scan_iter():
        time_data.set(key, int(time.time()))
        print(time_data.get(key).decode('utf-8'))


if __name__ == "__main__":
    main()
