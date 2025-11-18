import aiofiles
import os
from typing import Optional


async def async_file_operations(filename: str,
                                write_content: Optional[str] = None,
                                mode: str = 'r') -> str:
    try:
        if write_content is not None:
            async with aiofiles.open(filename, mode=mode) as file:
                await file.write(write_content)
                return f"Successfully wrote to {filename}"
        else:
            async with aiofiles.open(filename, mode='r') as file:
                content = await file.read()
                return content
    except Exception as e:
        raise Exception(f"Error during file operation: {str(e)}")