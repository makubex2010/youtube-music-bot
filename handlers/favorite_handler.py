from aiogram import F, Router
from aiogram.types import CallbackQuery, MessageReactionUpdated

from core.crud import get_by_attributes, get_or_create, remove
from core.db import async_session
from filters import Is_Thumbs_Down_Sign_Filter
from keyboards import favorites_keyboard
from models import Audio, User
from utils import MESSAGES, callback_message

router = Router(name="favorite_router")


@router.callback_query(F.data == "add_to_favorites")
async def add_to_favorites(callback: CallbackQuery):
    """Добавляет аудио в избранное."""

    async with async_session() as session:
        audio, flag = await get_or_create(
            session=session,
            model=Audio,
            user_id=callback.from_user.id,
            title=callback.message.audio.title or "Unknown audio"
        )
        if not flag:
            audio.message_id = callback.message.message_id
            await session.commit()

    if not flag:
        await callback_message(
            target=callback,
            text=MESSAGES["SUCCESS_ADDED_MSG"],
            reply_markup=favorites_keyboard()
        )
        return
    await callback_message(
        target=callback,
        text=MESSAGES["ALREADY_IN_FAVORITES"],
        reply_markup=favorites_keyboard()
    )


@router.callback_query(F.data == "get_favorites")
async def get_favorites(callback: CallbackQuery):
    """Показывает Избранные аудио данного пользователя."""

    async with async_session() as session:
        user, _ = await get_or_create(
            session=session,
            model=User,
            id=callback.from_user.id,
        )
        user_audios = user.audios
        if not user_audios:
            await callback_message(
                target=callback,
                text=MESSAGES["USER_DOES_NOT_HAVE_FAVS"],
            )
            return
        await callback.message.answer("Все Ваши Избранные:")
        for audio in user_audios:
            msg = await callback.message.bot.forward_messages(
                chat_id=callback.from_user.id,
                from_chat_id=callback.from_user.id,
                message_ids=[audio.message_id]
            )
            audio.forwarded_message_id = msg[0].message_id
        await session.commit()
    await callback.message.edit_reply_markup()


@router.message_reaction(Is_Thumbs_Down_Sign_Filter())
async def delete_audio(message_reaction: MessageReactionUpdated):
    """
    Удаляет аудио из Избранного, если поставлена
    соответствующая реакция.
    """

    async with async_session() as session:
        audio = await get_by_attributes(
            model=Audio,
            session=session,
            attributes={
                "user_id": message_reaction.user.id,
                "forwarded_message_id": message_reaction.message_id
            }
        )
        if not audio:
            await message_reaction.bot.send_message(
                text=MESSAGES["INCORRECT_REACTION"],
                chat_id=message_reaction.chat.id
            )
            return
        title = audio.title

        await remove(
            db_obj=audio,
            session=session
        )
    await message_reaction.bot.send_message(
        text=f'Аудио "{title}" успешно удалено из Избранного!',
        chat_id=message_reaction.chat.id,
        reply_markup=favorites_keyboard()
    )


@router.callback_query(F.data == "delete_button")
async def delete_keyboard(callback: CallbackQuery):
    """Удаляет клавиатуру."""

    await callback.message.edit_reply_markup()
