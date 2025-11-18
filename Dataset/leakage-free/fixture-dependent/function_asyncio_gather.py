import asyncio


def run_gather_tasks(*tasks):
    return asyncio.gather(*tasks)