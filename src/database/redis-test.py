import redis

social_data = redis.Redis(host='localhost', port=6379, db=0)
time_data = redis.Redis(host='localhost', port=6379, db=1)

result = social_data.json().get("377994022637010945")
print(result)
result = time_data.get("377994022637010945").decode('utf-8')
print(result)
