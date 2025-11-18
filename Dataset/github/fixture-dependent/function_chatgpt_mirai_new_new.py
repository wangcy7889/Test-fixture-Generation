from loguru import logger

async def preset_ask(self, role: str, text: str):
    if role.endswith('bot') or role in {'assistant', 'chatgpt'}:
        logger.debug(f'[预设] 响应：{text}')
        yield text
    else:
        logger.debug(f'[预设] 发送：{text}')
        item = None
        async for item in self.ask(text):
            ...
        if item:
            logger.debug(f'[预设] Chatbot 回应：{item}')