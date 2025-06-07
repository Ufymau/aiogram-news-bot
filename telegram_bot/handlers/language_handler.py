import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from db_peewee.db_users_class import save_user_to_db
from utils.languages import SELECTED_LANGUAGE_MESSAGES
from telegram_bot.middlewares.call_second_router_middleware import CallSecondRouterMiddleware
from telegram_bot.handlers.news_handlers import choose_news
from utils.logger_config import logger
from typing import Dict, Any


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
    logger.info("Handler language_chosen called")  # Проверка вызова
    lang_code = callback.data.split("_")[1]
    user = callback.from_user
    user_data: Dict[str, Any] = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": lang_code,  # сохраняем выбранный язык, а не telegram language_code
        "is_bot": user.is_bot,
    }
    logger.info("The process of adding a user to the database:", user_data)

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_user_to_db, user_data)

    await callback.message.answer(f"{SELECTED_LANGUAGE_MESSAGES.get(lang_code)}")
    await callback.answer()

language_router.callback_query.middleware(CallSecondRouterMiddleware(choose_news))
