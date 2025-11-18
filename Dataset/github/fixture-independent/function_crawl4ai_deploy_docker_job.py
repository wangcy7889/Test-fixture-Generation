from typing import Callable
from fastapi import APIRouter
_redis = None
_config = None
_token_dep: Callable = lambda: None
router = APIRouter()

def init_job_router(redis, config, token_dep) -> APIRouter:
    global _redis, _config, _token_dep
    _redis, _config, _token_dep = (redis, config, token_dep)
    return router