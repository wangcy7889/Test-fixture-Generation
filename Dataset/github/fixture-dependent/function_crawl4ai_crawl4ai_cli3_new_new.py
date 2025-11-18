import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from crawl4ai import BrowserProfiler
console = Console()

async def create_profile_interactive(profiler: BrowserProfiler):
    console.print(Panel("[bold cyan]Create Browser Profile[/bold cyan]\nThis will open a browser window for you to set up your identity.\nLog in to sites, adjust settings, then press 'q' to save.", border_style='cyan'))
    profile_name = Prompt.ask('[cyan]Enter profile name[/cyan]', default=f'profile_{int(time.time())}')
    console.print('[cyan]Creating profile...[/cyan]')
    console.print("[yellow]A browser window will open. After logging in to sites, press 'q' in this terminal to save.[/yellow]")
    try:
        profile_path = await profiler.create_profile(profile_name)
        if profile_path:
            console.print(f'[green]Profile successfully created at:[/green] {profile_path}')
        else:
            console.print('[red]Failed to create profile.[/red]')
    except Exception as e:
        console.print(f'[red]Error creating profile: {str(e)}[/red]')