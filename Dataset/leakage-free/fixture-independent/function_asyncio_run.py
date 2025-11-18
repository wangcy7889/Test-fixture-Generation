import asyncio

async def async_task(name, delay):
    await asyncio.sleep(delay)
    return f"Task {name} completed after {delay} seconds"

def run_async_task(name, delay):
    result = asyncio.run(async_task(name, delay))
    return result
