import time
import os
import redis
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# print("REDIS_HOST:", os.getenv("REDIS_HOST"))
cache = redis.Redis(
    host='srv-captain--redis',
    port=6379,
    password='MyBIPMPassword',
    decode_responses=True
)


app = Flask(__name__)

def get_hit_count():
    retries = 5
    while retries > 0:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            retries -= 1  # decrement retries!
            print(f"Redis connection failed: {type(exc).__name__} - {exc}. Retries left: {retries}")
            time.sleep(0.5)
    raise ConnectionError("Could not connect to Redis after multiple retries.")

@app.route('/')
def hello():
    try:
        count = get_hit_count()
    except Exception as e:
        count = 'N/A'
        print(f"Error getting hit count: {e}")
    return render_template('hello.html', name="BIPM", count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
