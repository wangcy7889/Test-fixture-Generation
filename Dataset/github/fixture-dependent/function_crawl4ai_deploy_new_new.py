import os
import logging
from fastapi import HTTPException, status
from crawl4ai import AsyncWebCrawler
from crawl4ai.utils import perform_completion_with_backoff
logger = logging.getLogger(__name__)

async def handle_llm_qa(url: str, query: str, config: dict) -> str:
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        last_q_index = url.rfind('?q=')
        if last_q_index != -1:
            url = url[:last_q_index]
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url)
            if not result.success:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result.error_message)
            content = result.markdown.fit_markdown or result.markdown.raw_markdown
        prompt = f'Use the following content as context to answer the question.\n    Content:\n    {content}\n\n    Question: {query}\n\n    Answer:'
        response = perform_completion_with_backoff(provider=config['llm']['provider'], prompt_with_variables=prompt, api_token=os.environ.get(config['llm'].get('api_key_env', '')))
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f'QA processing error: {str(e)}', exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))