import os
import re
import random
from typing import Optional, Dict
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def demo_proxy_rotation():
    print('\n=== 8. Proxy Rotation Demo ===')

    async def get_next_proxy(proxy_file: str='proxies.txt') -> Optional[Dict]:
        """Get next proxy from local file"""
        try:
            proxies = os.getenv('PROXIES', '').split(',')
            ip, port, username, password = random.choice(proxies).split(':')
            return {'server': f'http://{ip}:{port}', 'username': username, 'password': password, 'ip': ip}
        except Exception as e:
            print(f'Error loading proxy: {e}')
            return None
    urls = ['https://httpbin.org/ip'] * 2
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for url in urls:
            proxy = await get_next_proxy()
            if not proxy:
                print('No proxy available, skipping...')
                continue
            current_config = run_config.clone(proxy_config=proxy, user_agent='')
            result = await crawler.arun(url=url, config=current_config)
            if result.success:
                ip_match = re.search('(?:[0-9]{1,3}\\.){3}[0-9]{1,3}', result.html)
                print(f"Proxy {proxy['ip']} -> Response IP: {(ip_match.group(0) if ip_match else 'Not found')}")
                verified = ip_match.group(0) == proxy['ip']
                if verified:
                    print(f"✅ Proxy working! IP matches: {proxy['ip']}")
                else:
                    print('❌ Proxy failed or IP mismatch!')
            else:
                print(f"Failed with proxy {proxy['ip']}")