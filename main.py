import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import Config
from handlers import router


async def main() -> None:
    bot = Bot(token=Config.TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
