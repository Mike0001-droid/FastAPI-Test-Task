import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("sqlalchemy")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = RotatingFileHandler("back_logs/app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)

logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

logging.getLogger("sqlalchemy.orm").setLevel(logging.ERROR)

logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)