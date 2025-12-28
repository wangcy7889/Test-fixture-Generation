import hashlib
from pathlib import Path
from typing import Literal
import aiofiles
import aiofiles.os as aios
async def calc_hash(path: Path, hash_type: Literal["sha1", "sha256"] = "sha1") -> str:
    hasher = hashlib.sha1() if hash_type == "sha1" else hashlib.sha256()
    if hash_type == "sha1":
        header = f"blob {(await aios.stat(path)).st_size}\0".encode()
        hasher.update(header)
    async with aiofiles.open(path, "rb") as f:
        while chunk := await f.read(8 * 1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


