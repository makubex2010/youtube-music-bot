from re import search

from aiogram.filters import BaseFilter
from aiogram.types import Message


class Is_YT_URL_Filter(BaseFilter):
    """
    Фильтр для проверки корректности ссылки.
    """
    async def __call__(self, message: Message) -> bool:
        text = message.text or ""
        return bool(search(r"(youtube\.com|youtu\.be)", text))
