import os
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CacheMode

async def browser_management_example():
    user_data_dir = os.path.join(Path.home(), '.crawl4ai', 'browser_profile')
    os.makedirs(user_data_dir, exist_ok=True)
    print(f'Browser profile will be saved to: {user_data_dir}')
    async with AsyncWebCrawler(use_managed_browser=True, user_data_dir=user_data_dir, headless=False, verbose=True) as crawler:
        result = await crawler.arun(url='https://crawl4ai.com', cache_mode=CacheMode.BYPASS)
        result = await crawler.arun(url='https://github.com/trending', cache_mode=CacheMode.BYPASS)
        print('\nBrowser session result:', result.success)
        if result.success:
            print('Page title:', result.metadata.get('title', 'No title found'))