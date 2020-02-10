import redis
import time

conn = redis.Redis(host='127.0.0.1', port='6379')

conn.set('language', 'python')
print(conn.get("language"))

conn.set('language', 'python', px=10000)
print(conn.get('language'))
print(conn.ttl('language'))
time.sleep(3)
print(conn.ttl('language'))

conn.set('language', 'python', px=10000)
print(conn.expire('language', 10))
print(conn.ttl('language'))
time.sleep(3)
print(conn.ttl('language'))