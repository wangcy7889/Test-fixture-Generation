from pathlib import Path
import aiofiles.os as aios
async def get_downloaded_size(path: Path) -> int:
    partial_path = path.with_suffix(path.suffix + ".partial")
    if await aios.path.exists(path):
        return (await aios.stat(path)).st_size
    if await aios.path.exists(partial_path):
        return (await aios.stat(partial_path)).st_size
    return 0
