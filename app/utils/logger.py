from loguru import logger
from pathlib import Path

# Create logs folder if not exists
Path("logs").mkdir(exist_ok=True)

logger.remove()

logger.add(
    "logs/flowfi.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

logger.add(
    lambda msg: print(msg, end=""),
    level="INFO"
)
