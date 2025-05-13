from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def audio_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для работы с Аудио."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить в избранное",
            callback_data="add_to_favorites"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="delete_button"
        ),
    )
    return builder.as_markup()


def favorites_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для показа избранного"""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Перейти в Избранное",
            callback_data="get_favorites"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="delete_button"
        ),
    )
    return builder.as_markup()
