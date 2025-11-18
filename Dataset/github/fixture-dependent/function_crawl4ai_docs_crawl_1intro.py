from typing import List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeepCrawlStrategy, CrawlResult, FilterChain, DomainFilter, URLPatternFilter

async def basic_deep_crawl():
    url_filter = URLPatternFilter(patterns=['*text*'])
    domain_filter = DomainFilter(allowed_domains=['groq.com'], blocked_domains=['example.com'])
    config = CrawlerRunConfig(deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, max_pages=10, include_external=False, filter_chain=FilterChain(filters=[url_filter, domain_filter])), verbose=True)
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(url='https://console.groq.com/docs', config=config)
        for result in results:
            print(f"URL: {result.url}, Depth: {result.metadata.get('depth', 0)}")