from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LXMLWebScrapingStrategy

async def demo_content_scraping():
    print('\n=== 3. Content Scraping Strategy Demo ===')
    crawler = AsyncWebCrawler()
    url = 'https://example.com/article'
    config = CrawlerRunConfig(scraping_strategy=LXMLWebScrapingStrategy(), verbose=True)
    print('Scraping content with LXML strategy...')
    async with crawler:
        result = await crawler.arun(url, config=config)
        if result.success:
            print('Successfully scraped content using LXML strategy')