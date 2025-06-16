from typing import List, Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db_peewee.db_users_class import get_user_news_settings

keywords_router = Router()

@keywords_router.message(Command(commands=["selected_keyword"]))
async def selected_keywords_command(message: Message) -> None:
    """
        Outputs previously selected key values in /news_keyword

        Args:
            message (Message): The message object from the user.

        Returns:
            None
    """
    user_id = message.from_user.id
    news_choice, news_keywords = get_user_news_settings(user_id)

    await message.answer(news_keywords.replace(",", ", "))