
import os, json, redis
from typing import Any, Dict

def sync_redis_cache(key: str,
                     fetcher,
                     ttl: int = 60,
                     env_url: str = 'REDIS_URL') -> Dict[str, Any]:
    url = os.getenv(env_url)
    if not url:
        raise EnvironmentError('Error: REDIS_URL is not set')
    r = redis.Redis.from_url(url, decode_responses=True)

    val = r.get(key)
    if val:
        return json.loads(val)

    data = fetcher()
    r.setex(key, ttl, json.dumps(data, ensure_ascii=False))
    return data
