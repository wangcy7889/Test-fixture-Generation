from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DisplayMode, MemoryAdaptiveDispatcher, CrawlerMonitor, DefaultMarkdownGenerator

async def demo_memory_dispatcher():
    print('\n=== Memory Dispatcher Demo ===')
    try:
        browser_config = BrowserConfig(headless=True, verbose=False)
        crawler_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, markdown_generator=DefaultMarkdownGenerator())
        urls = ['http://example.com', 'http://example.org', 'http://example.net'] * 3
        print('\n📈 Initializing crawler with memory monitoring...')
        async with AsyncWebCrawler(config=browser_config) as crawler:
            monitor = CrawlerMonitor(max_visible_rows=10, display_mode=DisplayMode.DETAILED)
            dispatcher = MemoryAdaptiveDispatcher(memory_threshold_percent=80.0, check_interval=0.5, max_session_permit=5, monitor=monitor)
            print('\n🚀 Starting batch crawl...')
            results = await crawler.arun_many(urls=urls, config=crawler_config, dispatcher=dispatcher)
            print(f'\n✅ Completed {len(results)} URLs successfully')
    except Exception as e:
        print(f'\n❌ Error in memory dispatcher demo: {str(e)}')