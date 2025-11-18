import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def demo_ssl_features():
    print('\n1. Enhanced SSL & Security Demo')
    print('--------------------------------')
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, fetch_ssl_certificate=True)
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url='https://example.com', config=run_config)
        print(f'SSL Crawl Success: {result.success}')
        result.ssl_certificate.to_json(os.path.join(os.getcwd(), 'ssl_certificate.json'))
        if not result.success:
            print(f'SSL Error: {result.error_message}')