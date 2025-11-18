import asyncio
from loguru import logger

def retry(exceptions, tries=4, delay=3, backoff=2):

    def decorator(func):

        async def wrapper(*args, **kwargs):
            _tries = tries
            _delay = delay
            while _tries > 0:
                try:
                    async for result in func(*args, **kwargs):
                        yield result
                    return
                except exceptions as e:
                    logger.exception(e)
                    logger.error(f'处理请求时遇到错误, 将在 {_delay} 秒后重试...')
                    await asyncio.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            async for result in func(*args, **kwargs):
                yield result
        return wrapper
    return decorator