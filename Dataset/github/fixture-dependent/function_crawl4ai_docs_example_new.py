import httpx
import os
from rich.console import Console
console = Console()
BASE_URL = os.getenv('CRAWL4AI_TEST_URL', 'http://localhost:8020')

async def check_server_health(client: httpx.AsyncClient):
    console.print('[bold cyan]Checking server health...[/]', end='')
    try:
        response = await client.get('/health', timeout=10.0)
        response.raise_for_status()
        health_data = response.json()
        console.print(f"[bold green] Server OK! Version: {health_data.get('version', 'N/A')}[/]")
        return True
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        console.print(f'\n[bold red]Server health check FAILED:[/]')
        console.print(f'Error: {e}')
        console.print(f'Is the server running at {BASE_URL}?')
        return False
    except Exception as e:
        console.print(f'\n[bold red]An unexpected error occurred during health check:[/]')
        console.print(e)
        return False