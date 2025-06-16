from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.languages import LANGUAGES

help_lang = ", ".join(LANGUAGES.values())

help_router = Router()

@help_router.message(Command(commands=["help"]))
async def help_handler(message: Message) -> None:
    """
        Handler for the /help command.

        Args:
            message (Message): Incoming message with /help command.

        Returns:
            None
    """
    help_text = (
        "👋👋👋Hi! I am a news bot.👋👋👋\n\n"
        "Available commands:\n\n" 
        "▶️ /start — Start the bot and select the language.\n"
            f"(Supported languages: {help_lang})\n\n"
        "🆘 /help — This is help! A list of all my commands.\n\n" 
        "🗞 /news_all — Follow all the latest news today! 👁\n\n" 
        "🗞 /news_keyword - Follow the news today by their keywords! 🗝\n\n"
        "🗞 /selected_keyword - Outputs previously selected keywords in (news_keyword) 🗝\n\n"
        "👀 Glad to see you here 👀"
    )
    await message.answer(help_text)

