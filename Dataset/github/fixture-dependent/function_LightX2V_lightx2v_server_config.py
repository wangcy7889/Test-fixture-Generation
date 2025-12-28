import os
from loguru import logger
def from_env(cls) -> "ServerConfig":
        config = cls()
        if env_host := os.environ.get("LIGHTX2V_HOST"):
            config.host = env_host
        if env_port := os.environ.get("LIGHTX2V_PORT"):
            try:
                config.port = int(env_port)
            except ValueError:
                logger.warning(f"Invalid port in environment: {env_port}")
        if env_queue_size := os.environ.get("LIGHTX2V_MAX_QUEUE_SIZE"):
            try:
                config.max_queue_size = int(env_queue_size)
            except ValueError:
                logger.warning(f"Invalid max queue size: {env_queue_size}")
        if env_cache_dir := os.environ.get("LIGHTX2V_CACHE_DIR"):
            config.cache_dir = env_cache_dir
        return config
