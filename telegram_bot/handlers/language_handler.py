from typing import Any, Dict

from aiogram import F, Router
from aiogram.types import CallbackQuery
import asyncio

from db_peewee.db_users_class import save_user_to_db
from telegram_bot.handlers.news_handlers import choose_news
from telegram_bot.middlewares.call_second_router_middleware import CallSecondRouterMiddleware
from utils.languages import SELECTED_LANGUAGE_MESSAGES
from utils.logger_config import logger

language_router = Router()

@language_router.callback_query(F.data.startswith("lang_"))
async def language_chosen(callback: CallbackQuery) -> None:
    """
        Handler for callback queries where data starts with "lang_".
        Extracts the language code from the callback data, constructs user data,
        saves the user information to the database asynchronously, and sends a confirmation message.

        Args:
            callback (CallbackQuery): Incoming callback query from the user.

        Returns:
            None
    """
    logger.info("Handler language_chosen called")
    lang_code = callback.data.split("_")[1]
    user = callback.from_user
    user_data: Dict[str, Any] = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": lang_code,
        "is_bot": user.is_bot,
    }
    logger.info("The process of adding a user to the database:", user_data)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_user_to_db, user_data)

    await callback.message.answer(f"{SELECTED_LANGUAGE_MESSAGES.get(lang_code)}")
    await callback.answer()

language_router.callback_query.middleware(CallSecondRouterMiddleware(choose_news))
