from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, MemoryAdaptiveDispatcher

async def demo_streaming_support():
    print('\n=== 2. Streaming Support Demo ===')
    browser_config = BrowserConfig(headless=True, verbose=False)
    crawler_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)
    urls = ['http://example.com', 'http://example.org', 'http://example.net'] * 2
    async with AsyncWebCrawler(config=browser_config) as crawler:
        dispatcher = MemoryAdaptiveDispatcher(max_session_permit=3, check_interval=0.5)
        print('Starting streaming crawl...')
        async for result in await crawler.arun_many(urls=urls, config=crawler_config, dispatcher=dispatcher):
            print(f'Received result for {result.url} - Success: {result.success}')
            if result.success:
                print(f'Content length: {len(result.markdown)}')