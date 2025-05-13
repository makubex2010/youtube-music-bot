from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.crud import get_or_create
from core.db import async_session
from models import User
from utils import MESSAGES, callback_message, init_user

router = Router(name="cmd_router")


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    """
    Обработчик команды /start для нового пользователя.
    Инициализирует пользователя в БД и выводит 
    приветственное сообщение.
    """

    async with async_session() as session:
        await init_user(
            session=session,
            user_id=message.from_user.id,
            username=message.from_user.username
        )
    await message.answer(
        MESSAGES["START_MSG"].format(name=message.chat.full_name)
    )


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    """Обработчик команды /help."""

    await message.answer(MESSAGES["HELP_MSG"])


@router.message(Command(commands=["favorites"]))
async def cmd_get_favs(message: Message):
    """
    Обработчик команды /favorites.
    Выводит Избранные аудио пользователя
    или сообщает что их нет.
    """

    async with async_session() as session:
        user, _ = await get_or_create(
            session=session,
            model=User,
            id=message.from_user.id,
        )
        user_audios = user.audios
        if not user_audios:
            await callback_message(
                target=message,
                text=MESSAGES["USER_DOES_NOT_HAVE_FAVS"],
                delete_reply=False
            )
            return
        await message.answer("Все Ваши Избранные:")
        for audio in user_audios:
            msg = await message.bot.forward_messages(
                chat_id=message.from_user.id,
                from_chat_id=message.from_user.id,
                message_ids=[audio.message_id]
            )
            audio.forwarded_message_id = msg[0].message_id
        await session.commit()
