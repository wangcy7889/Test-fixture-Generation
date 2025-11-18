import asyncio, time
import httpx
from rich.console import Console
console = Console()

async def poll_for_result(client: httpx.AsyncClient, task_id: str, poll_interval: float=1.5, timeout: float=90.0):
    start = time.time()
    while True:
        resp = await client.get(f'/crawl/job/{task_id}')
        resp.raise_for_status()
        data = resp.json()
        status = data.get('status')
        if status.upper() in ('COMPLETED', 'FAILED'):
            return data
        if time.time() - start > timeout:
            raise TimeoutError(f'Task {task_id} did not finish in {timeout}s')
        await asyncio.sleep(poll_interval)