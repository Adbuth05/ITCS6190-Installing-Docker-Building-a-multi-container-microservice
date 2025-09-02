import time
import redis
from flask import Flask

app = Flask(__name__)
# Important: host='redis' matches the service name in compose.yaml
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    # simple retry loop while Redis starts up
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return f"Hello World! I have been seen {count} times.\n"
