import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, DefaultMarkdownGenerator, LLMContentFilter

async def demo_llm_markdown():
    print('\n=== 4. LLM-Powered Markdown Generation Demo ===')
    crawler = AsyncWebCrawler()
    url = 'https://docs.python.org/3/tutorial/classes.html'
    content_filter = LLMContentFilter(provider='openai/gpt-4o', api_token=os.getenv('OPENAI_API_KEY'), instruction='\n        Focus on extracting the core educational content about Python classes.\n        Include:\n        - Key concepts and their explanations\n        - Important code examples\n        - Essential technical details\n        Exclude:\n        - Navigation elements\n        - Sidebars\n        - Footer content\n        - Version information\n        - Any non-essential UI elements\n\n        Format the output as clean markdown with proper code blocks and headers.\n        ', verbose=True)
    config = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator(content_filter=content_filter), cache_mode=CacheMode.BYPASS, verbose=True)
    print('Generating focused markdown with LLM...')
    async with crawler:
        result = await crawler.arun(url, config=config)
        if result.success and result.markdown_v2:
            print('Successfully generated LLM-filtered markdown')
            print('First 500 chars of filtered content:')
            print(result.markdown_v2.fit_markdown[:500])
            print('Successfully generated LLM-filtered markdown')