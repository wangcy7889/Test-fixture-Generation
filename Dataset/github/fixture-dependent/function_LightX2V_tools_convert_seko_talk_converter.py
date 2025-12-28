import subprocess
from loguru import logger
def run_command(cmd: list, description: str):
    logger.info(f"\n{description}")
    logger.info("Command: " + " \\\n  ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"{description} FAILED!")
        logger.error(f"STDOUT:\n{result.stdout}")
        logger.error(f"STDERR:\n{result.stderr}")
        raise RuntimeError(f"{description} failed")
    logger.info(f"✓ {description} completed!")
    return result

