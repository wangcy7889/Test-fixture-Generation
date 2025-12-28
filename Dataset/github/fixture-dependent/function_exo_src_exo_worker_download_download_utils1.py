import ssl
from typing import Literal
import aiohttp
import certifi
def create_http_session(
    auto_decompress: bool = False,
    timeout_profile: Literal["short", "long"] = "long",
) -> aiohttp.ClientSession:
    if timeout_profile == "short":
        total_timeout = 30
        connect_timeout = 10
        sock_read_timeout = 30
        sock_connect_timeout = 10
    else:
        total_timeout = 1800
        connect_timeout = 60
        sock_read_timeout = 1800
        sock_connect_timeout = 60

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    return aiohttp.ClientSession(
        auto_decompress=auto_decompress,
        connector=connector,
        timeout=aiohttp.ClientTimeout(
            total=total_timeout,
            connect=connect_timeout,
            sock_read=sock_read_timeout,
            sock_connect=sock_connect_timeout,
        ),
    )

