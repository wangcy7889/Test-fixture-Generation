import httpx
import time
import urllib.parse
from rich.console import Console
from rich.panel import Panel
console = Console()
SIMPLE_URL = 'https://httpbin.org/html'

async def demo_llm_endpoint(client: httpx.AsyncClient):
    page_url = SIMPLE_URL
    question = 'What is the title of this page?'
    console.rule('[bold magenta]Demo 7b: /llm Endpoint[/]', style='magenta')
    enc = urllib.parse.quote_plus(page_url, safe='')
    console.print(f'GET /llm/{enc}?q={question}')
    try:
        t0 = time.time()
        resp = await client.get(f'/llm/{enc}', params={'q': question})
        dt = time.time() - t0
        console.print(f"Response Status: [bold {('green' if resp.is_success else 'red')}]{resp.status_code}[/] (took {dt:.2f}s)")
        resp.raise_for_status()
        answer = resp.json().get('answer', '')
        console.print(Panel(answer or 'No answer returned', title='LLM answer', border_style='magenta', expand=False))
    except Exception as e:
        console.print(f'[bold red]Error hitting /llm:[/] {e}')