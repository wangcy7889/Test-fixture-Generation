import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy

async def demo_json_schema_generation():
    print('\n=== 7. LLM-Powered Schema Generation Demo ===')
    html_content = '\n    <div class="job-listing">\n        <h1 class="job-title">Senior Software Engineer</h1>\n        <div class="job-details">\n            <span class="location">San Francisco, CA</span>\n            <span class="salary">$150,000 - $200,000</span>\n            <div class="requirements">\n                <h2>Requirements</h2>\n                <ul>\n                    <li>5+ years Python experience</li>\n                    <li>Strong background in web crawling</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n    '
    print('Generating CSS selectors schema...')
    css_schema = JsonCssExtractionStrategy.generate_schema(html_content, schema_type='CSS', query='Extract job title, location, and salary information', provider='openai/gpt-4o')
    print('\nGenerated CSS Schema:')
    print(css_schema)
    crawler = AsyncWebCrawler()
    url = 'https://example.com/job-listing'
    extraction_strategy = JsonCssExtractionStrategy(schema=css_schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy, verbose=True)
    print('\nTesting generated schema with crawler...')
    async with crawler:
        result = await crawler.arun(url, config=config)
        if result.success:
            print(json.dumps(result.extracted_content, indent=2) if result.extracted_content else None)
            print('Successfully used generated schema for crawling')