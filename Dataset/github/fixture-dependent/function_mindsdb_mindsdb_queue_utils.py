import time
from walrus import Database
from redis.exceptions import ConnectionError as RedisConnectionError

def wait_redis_ping(db: Database, timeout: int=30):
    end_time = time.time() + timeout
    while time.time() <= end_time:
        try:
            if db.ping() is True:
                break
        except RedisConnectionError:
            pass
        time.sleep(2)
    else:
        raise RedisConnectionError