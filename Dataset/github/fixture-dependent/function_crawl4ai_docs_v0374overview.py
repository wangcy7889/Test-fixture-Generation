import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_parent_dir = os.path.dirname(parent_dir)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CacheMode

async def download_example():
    downloads_path = os.path.join(Path.home(), '.crawl4ai', 'downloads')
    os.makedirs(downloads_path, exist_ok=True)
    print(f'Downloads will be saved to: {downloads_path}')
    async with AsyncWebCrawler(accept_downloads=True, downloads_path=downloads_path, verbose=True) as crawler:
        result = await crawler.arun(url='https://www.python.org/downloads/', js_code='\n            // Find and click the first Windows installer link\n            const downloadLink = document.querySelector(\'a[href$=".exe"]\');\n            if (downloadLink) {\n                console.log(\'Found download link:\', downloadLink.href);\n                downloadLink.click();\n            } else {\n                console.log(\'No .exe download link found\');\n            }\n            ', delay_before_return_html=1, cache_mode=CacheMode.BYPASS)
        if result.downloaded_files:
            print('\nDownload successful!')
            print('Downloaded files:')
            for file_path in result.downloaded_files:
                print(f'- {file_path}')
                print(f'  File size: {os.path.getsize(file_path) / (1024 * 1024):.2f} MB')
        else:
            print('\nNo files were downloaded')