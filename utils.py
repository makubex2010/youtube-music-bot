from os import path
from re import sub
from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardMarkup

from core.crud import get_or_create
from models import User

MESSAGES = {
    "FIRST_MSG": "Скачиваю аудио...",
    "SECOND_MSG": (
        "Аудио слишком длинное, разбиваю на части. "
        "Пожалуйста, подождите, это может занять много времени..."
    ),
    "SUCCESS_MSG": "Успешно отправлено!",
    "STREAM_MSG": "Я не умею работать со стримами =(",
    "ERROR_MSG": "Произошла ошибка",
    "USER_DOES_NOT_HAVE_FAVS": "У вас нет Избранных аудио =(",
    "ALREADY_IN_FAVORITES": "Эта аудиозапись уже в Избранном",
    "SUCCESS_ADDED_MSG": "Успешно добавлено в Избранное!",
    "INCORRECT_REACTION": "Я работаю только с 👎 на избранных аудио",
    "START_MSG": (
        "Привет, {name}. Я — бот, который поможет тебе скачивать аудио из "
        "YouTube-видео или шортсов и сохранять их прямо здесь, в Telegram\n\n"
        "Я умею:\n• Загружать аудио с YouTube по ссылке \n"
        "• Сохранять аудио в избранное и показывать их когда захочешь\n"
        "Просто пришли мне ссылку на YouTube — я всё сделаю сам!\n\n"
        "создатель @nilotan"
    ),
    "HELP_MSG": (
        "Привет!\n"
        "Просто пришли ссылку на YouTube — я скачаю аудио и отправлю тебе. "
        "Возможно, это займет некоторое время.\n\n"
        "Нажми кнопку «Добавить в избранное» под полученным аудио, чтобы "
        "сохранить его.\n"
        "Поставь 👎 на аудио в избранном, чтобы удалить его оттуда\n\n"
        "Команды:\n"
        "• /start — приветственное сообщение\n"
        "• /help — это сообщение\n"
        "• /favorites — список избранных аудио\n"
        "Если что-то пошло не так — попробуй ещё раз или напиши команду "
        "/help.\n\n"
        "Если у Вас есть пожелания или предложения связаться "
        "с создателем @nilotan"
    ),
}


async def callback_message(
    target: Union[Message, CallbackQuery],
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    replace_message: bool = False,
    delete_reply: bool = True,
    **kwargs,
):
    """Редактировние сообщения."""

    target = target if isinstance(target, Message) else target.message

    if replace_message:
        await target.edit_text(
            text=text,
            reply_markup=reply_markup,
            **kwargs
        )
    else:
        await target.answer(
            text=text,
            reply_markup=reply_markup,
            **kwargs
        )
        await target.delete_reply_markup() if delete_reply else None


def get_ydl_opts(tmpdir):
    """Настройки для работы с YoutubeDL."""

    return {
        "format": "bestaudio/best",
        "restrictfilenames": True,
        "noplaylist": True,
        "outtmpl": path.join(tmpdir, "%(title)s%(ext)s"),
        "quiet": True,
        "cachedir": path.join(tmpdir, "cache"),
    }


def sanitize_filename(s: str) -> str:
    """Преобразует название файла к корректному значению."""

    return sub(r"[^а-яА-Яa-zA-Z0-9]", "_", s)


async def init_user(session, user_id, username):
    """Инициализирует пользователя в БД."""

    user, _ = await get_or_create(
        session=session,
        model=User,
        id=user_id,
    )
    user.username = username
    await session.commit()
