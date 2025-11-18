import click
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def run_crawler(url: str, browser_cfg: BrowserConfig, crawler_cfg: CrawlerRunConfig, verbose: bool):
    if verbose:
        click.echo('Starting crawler with configurations:')
        click.echo(f'Browser config: {browser_cfg.dump()}')
        click.echo(f'Crawler config: {crawler_cfg.dump()}')
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        try:
            result = await crawler.arun(url=url, config=crawler_cfg)
            return result
        except Exception as e:
            raise click.ClickException(f'Crawling failed: {str(e)}')