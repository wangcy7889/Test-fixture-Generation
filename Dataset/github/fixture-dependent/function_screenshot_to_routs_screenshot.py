from typing import Awaitable, Callable, List, cast
from anthropic import AsyncAnthropic
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionChunk
MODEL_GPT_4_VISION = 'gpt-4-vision-preview'
MODEL_CLAUDE_SONNET = 'claude-3-sonnet-20240229'
MODEL_CLAUDE_OPUS = 'claude-3-opus-20240229'

async def stream_claude_response(messages: List[ChatCompletionMessageParam], api_key: str, callback: Callable[[str], Awaitable[None]]) -> str:
    client = AsyncAnthropic(api_key=api_key)
    model = MODEL_CLAUDE_SONNET
    max_tokens = 4096
    temperature = 0.0
    system_prompt = cast(str, messages[0]['content'])
    claude_messages = [dict(message) for message in messages[1:]]
    for message in claude_messages:
        if not isinstance(message['content'], list):
            continue
        for content in message['content']:
            if content['type'] == 'image_url':
                content['type'] = 'image'
                image_data_url = cast(str, content['image_url']['url'])
                media_type = image_data_url.split(';')[0].split(':')[1]
                base64_data = image_data_url.split(',')[1]
                del content['image_url']
                content['source'] = {'type': 'base64', 'media_type': media_type, 'data': base64_data}
    async with client.messages.stream(model=model, max_tokens=max_tokens, temperature=temperature, system=system_prompt, messages=claude_messages) as stream:
        async for text in stream.text_stream:
            await callback(text)
    response = await stream.get_final_message()
    return response.content[0].text