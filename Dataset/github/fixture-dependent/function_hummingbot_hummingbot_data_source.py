import asyncio
from typing import AsyncIterable
import websockets
from websockets.exceptions import ConnectionClosed

async def _inner_messages(self, ws: websockets.WebSocketClientProtocol) -> AsyncIterable[str]:
    try:
        while True:
            try:
                msg: str = await asyncio.wait_for(ws.recv(), timeout=self.MESSAGE_TIMEOUT)
                yield msg
            except asyncio.TimeoutError:
                pong_waiter = await ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=self.PING_TIMEOUT)
    except asyncio.TimeoutError:
        self.logger().warning('WebSocket ping timed out. Going to reconnect...')
        return
    except ConnectionClosed:
        return
    finally:
        await ws.close()