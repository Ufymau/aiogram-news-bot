import asyncio
from telegram_bot.create_bot import bot
from db_peewee.db_users_class import UserDB
from utils.news_sort import get_all_daily, get_key_daily
from utils.data_sort import split_messages
from typing import Optional, List
from utils.logger_config import logger

logger.info("Start logging auto send news")

async def send_news_to_user(user: UserDB) -> None:
    """
        Send news messages to a single user based on their preferences.

        Args:
            user (UserDB): User database model instance containing user preferences.

        Returns:
            None
    """
    try:
        chat_id: int = UserDB.user_id
        choice: Optional[str] = UserDB.news_choice
        keywords: Optional[str] = UserDB.news_keywords

        if choice == "news_all":
            news_messages: List[str] = get_all_daily()
        elif choice == "news_keyword" and keywords:
            keys_list: List[str] = [k.strip() for k in keywords.split(",") if k.strip()]
            news_messages = get_key_daily(keys_list)
        else:
            # If no choice is made, send default news
            news_messages = get_all_daily()

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