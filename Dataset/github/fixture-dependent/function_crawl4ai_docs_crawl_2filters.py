import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BFSDeepCrawlStrategy, CrawlResult, ContentTypeFilter, DomainFilter, FilterChain, URLPatternFilter

async def deep_crawl_filter_tutorial_part_2():
    print('\n' + '=' * 40)
    print('=== Introduction: URL Filters in Isolation ===')
    print('=' * 40 + '\n')
    print('In this section, we will explore each filter individually using synthetic URLs.')
    print('This allows us to understand exactly how each filter works before using them in a crawl.\n')
    print('\n' + '=' * 40)
    print('=== 2. ContentTypeFilter - Testing in Isolation ===')
    print('=' * 40 + '\n')
    content_type_filter = ContentTypeFilter(allowed_types=['text/html', 'application/json'])
    print("ContentTypeFilter created, allowing types (by extension): ['text/html', 'application/json']")
    print('Note: ContentTypeFilter in Crawl4ai works by checking URL file extensions, not HTTP headers.')
    test_urls_content_type = ['https://example.com/page.html', 'https://example.com/data.json', 'https://example.com/image.png', 'https://example.com/document.pdf', 'https://example.com/page', 'https://example.com/page.xhtml']
    print('\n=== Testing ContentTypeFilter (URL Extension based) ===')
    for url in test_urls_content_type:
        passed = content_type_filter.apply(url)
        result = 'PASSED' if passed else 'REJECTED'
        extension = ContentTypeFilter._extract_extension(url)
        print(f"- URL: {url} - {result} (Extension: '{extension or 'No Extension'}')")
    print('=' * 40)
    input('Press Enter to continue to DomainFilter example...')
    print('\n' + '=' * 40)
    print('=== 3. DomainFilter - Testing in Isolation ===')
    print('=' * 40 + '\n')
    domain_filter = DomainFilter(allowed_domains=['crawl4ai.com', 'example.com'])
    print("DomainFilter created, allowing domains: ['crawl4ai.com', 'example.com']")
    test_urls_domain = ['https://docs.crawl4ai.com/api', 'https://example.com/products', 'https://another-website.org/blog', 'https://sub.example.com/about', 'https://crawl4ai.com.attacker.net']
    print('\n=== Testing DomainFilter ===')
    for url in test_urls_domain:
        passed = domain_filter.apply(url)
        result = 'PASSED' if passed else 'REJECTED'
        print(f'- URL: {url} - {result}')
    print('=' * 40)
    input('Press Enter to continue to FilterChain example...')
    print('\n' + '=' * 40)
    print('=== 4. FilterChain - Combining Filters ===')
    print('=' * 40 + '\n')
    combined_filter = FilterChain(filters=[URLPatternFilter(patterns=['*api*']), ContentTypeFilter(allowed_types=['text/html']), DomainFilter(allowed_domains=['docs.crawl4ai.com'])])
    print('FilterChain created, combining URLPatternFilter, ContentTypeFilter, and DomainFilter.')
    test_urls_combined = ['https://docs.crawl4ai.com/api/async-webcrawler', 'https://example.com/api/products', 'https://docs.crawl4ai.com/core/crawling', 'https://another-website.org/api/data']
    print('\n=== Testing FilterChain (URLPatternFilter + ContentTypeFilter + DomainFilter) ===')
    for url in test_urls_combined:
        passed = await combined_filter.apply(url)
        result = 'PASSED' if passed else 'REJECTED'
        print(f'- URL: {url} - {result}')
    print('=' * 40)
    input('Press Enter to continue to Deep Crawl with FilterChain example...')
    print('\n' + '=' * 40)
    print('=== 5. Deep Crawl with FilterChain ===')
    print('=' * 40 + '\n')
    print("Finally, let's integrate the FilterChain into a deep crawl example.")
    config_final_crawl = CrawlerRunConfig(deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, max_pages=10, include_external=False, filter_chain=combined_filter), verbose=False)
    async with AsyncWebCrawler() as crawler:
        results_final_crawl: List[CrawlResult] = await crawler.arun(url='https://docs.crawl4ai.com', config=config_final_crawl)
        print('=== Crawled URLs (Deep Crawl with FilterChain) ===')
        for result in results_final_crawl:
            print(f"- {result.url}, Depth: {result.metadata.get('depth', 0)}")
        print('=' * 40)
    print('\nTutorial Completed! Review the output of each section to understand URL filters.')