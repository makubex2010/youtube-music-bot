import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    MAX_SIZE: int = 49 * 1024 * 1024  # 49 МБ

    TOKEN: str = str(os.getenv("BOT_TOKEN"))
    DB_URL: str = os.getenv("DB_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
