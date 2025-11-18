import os
from typing import List, Dict
from rich.console import Console
console = Console()

def load_proxies_from_env() -> List[Dict]:
    proxies_params_list = []
    proxies_str = os.getenv('PROXIES', '')
    if not proxies_str:
        return proxies_params_list
    try:
        proxy_entries = proxies_str.split(',')
        for entry in proxy_entries:
            entry = entry.strip()
            if not entry:
                continue
            parts = entry.split(':')
            proxy_dict = {}
            if len(parts) == 4:
                ip, port, username, password = parts
                proxy_dict = {'server': f'http://{ip}:{port}', 'username': username, 'password': password}
            elif len(parts) == 2:
                ip, port = parts
                proxy_dict = {'server': f'http://{ip}:{port}'}
            else:
                console.print(f'[yellow]Skipping invalid proxy string format:[/yellow] {entry}')
                continue
            proxies_params_list.append(proxy_dict)
    except Exception as e:
        console.print(f'[red]Error loading proxies from environment:[/red] {e}')
    if proxies_params_list:
        console.print(f'[cyan]Loaded {len(proxies_params_list)} proxies from environment.[/]')
    return proxies_params_list