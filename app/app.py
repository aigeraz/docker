import time
import os
import redis
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup Redis connection
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True  # Optional: makes Redis return strings not bytes
)

app = Flask(__name__)

def get_hit_count():
    retries = 5
    while retries > 0:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            retries -= 1
            print(f"Redis connection failed, retries left: {retries}")
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
