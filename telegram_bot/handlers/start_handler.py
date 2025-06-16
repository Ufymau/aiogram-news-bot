from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_bot.keyboards.lang_keyboard import language_keyboard
from utils.logger_config import logger

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
        Handler for the /start command.
        Sends a greeting message and prompts the user to choose their language
        using an inline keyboard.

        Args:
            message (Message): Incoming message with the /start command.

        Returns:
            None
    """

    logger.info("Handler start_chosen called")
    await message.answer(
        "Hello! Please choose your language: 🌐🧐",
        reply_markup=language_keyboard()
    )

