from litellm import completion

async def stream_llm_response(url: str, markdown: str, query: str, provider: str, token: str):
    response = completion(model=provider, api_key=token, messages=[{'content': f'You are Crawl4ai assistant, answering user question based on the provided context which is crawled from {url}.', 'role': 'system'}, {'content': f'<|start of context|>\n{markdown}\n<|end of context|>\n\n{query}', 'role': 'user'}], stream=True)
    for chunk in response:
        if (content := chunk['choices'][0]['delta'].get('content')):
            print(content, end='', flush=True)
    print()