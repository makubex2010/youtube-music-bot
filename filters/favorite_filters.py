from aiogram.filters import BaseFilter
from aiogram.types import MessageReactionUpdated, ReactionTypeEmoji

from utils import MESSAGES


class Is_Thumbs_Down_Sign_Filter(BaseFilter):
    """
    Фильтр для проверки корректности поставленной реакции.
    """
    async def __call__(self, message_reaction: MessageReactionUpdated) -> bool:
        reaction = message_reaction.new_reaction
        if not reaction:
            return False
        if reaction[0].emoji != "👎":
            await message_reaction.bot.send_message(
                text=MESSAGES["INCORRECT_REACTION"],
                chat_id=message_reaction.chat.id
            )
            return False
        return (
            isinstance(reaction[0], ReactionTypeEmoji) and
            reaction[0].emoji == "👎"
        )
