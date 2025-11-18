import os
import asyncio
import aiohttp
import json

async def api_example():
    api_token = os.getenv('CRAWL4AI_API_TOKEN') or 'test_api_code'
    headers = {'Authorization': f'Bearer {api_token}'}
    async with aiohttp.ClientSession() as session:
        crawl_request = {'urls': ['https://news.ycombinator.com'], 'extraction_config': {'type': 'json_css', 'params': {'schema': {'name': 'Hacker News Articles', 'baseSelector': '.athing', 'fields': [{'name': 'title', 'selector': '.title a', 'type': 'text'}, {'name': 'score', 'selector': '.score', 'type': 'text'}, {'name': 'url', 'selector': '.title a', 'type': 'attribute', 'attribute': 'href'}]}}}, 'crawler_params': {'headless': True}, 'cache_mode': 'bypass'}
        async with session.post('http://localhost:11235/crawl', json=crawl_request, headers=headers) as response:
            task_data = await response.json()
            task_id = task_data['task_id']
            while True:
                async with session.get(f'http://localhost:11235/task/{task_id}', headers=headers) as status_response:
                    result = await status_response.json()
                    print(f"Task status: {result['status']}")
                    if result['status'] == 'completed':
                        print('Task completed!')
                        print('Results:')
                        news = json.loads(result['results'][0]['extracted_content'])
                        print(json.dumps(news[:4], indent=2))
                        break
                    else:
                        await asyncio.sleep(1)