from typing import List, Optional, Union

import asyncio

from db_peewee.db_users_class import UserDB
from telegram_bot.create_bot import bot
from utils.data_sort import split_messages
from utils.logger_config import logger
from utils.news_sort import get_all_daily, get_key_daily

async def send_news_to_user(user: UserDB) -> None:
    """
        Send news messages to a single user based on their preferences.

        Args:
            user (UserDB): User database model instance containing user preferences.

        Returns:
            None
    """
    try:
        chat_id: int = user.user_id
        choice: str = user.news_choice
        keywords: Optional[Union[str, List[str]]] = user.news_keywords
        lang_code: str = user.language_code

        if choice == "news_all":
            news_messages: List[str] = get_all_daily(lang_code=lang_code)
        elif choice == "news_keyword" and keywords:
            keys_list: List[str] = [k.strip() for k in keywords.split(",") if k.strip()]
            news_messages = get_key_daily(keys_list, lang_code=lang_code)
        else:
            # If no choice is made, send default news
            news_messages = get_all_daily(lang_code=lang_code)

        messages: List[str] = split_messages(news_messages)
        for msg in messages:
            await bot.send_message(chat_id, msg, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error sending news to the user {UserDB.user_id}: {e}")


async def send_news_to_all_users() -> None:
    """
        Send news to all users in the database concurrently.

        Returns:
            None
    """
    users = UserDB.select()
    tasks = [send_news_to_user(user) for user in users]
    await asyncio.gather(*tasks)  # Run sending asynchronously


async def schedule_news_send() -> None:
    """
        Schedule the news sending process, logging start and completion.

        Returns:
            None
    """
    try:
        logger.info("Start of the newsletter")
        await send_news_to_all_users()
        logger.info("The newsletter has been completed")
    except Exception as e:
        logger.error(f"Newsletter error: {e}")