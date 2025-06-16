from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

router1 = Router()

@router1.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
        Handler for the /start command.

        Args:
            message (Message): Incoming message with /start command.

        Returns:
            None
    """
    await message.answer("Hello!")

router2 = Router()

@router2.message(Command(commands=["help"]))
async def help_handler(message: Message) -> None:
    """
        Handler for the /help command.

        Args:
            message (Message): Incoming message with /help command.

        Returns:
            None
    """
    await message.answer("Help")

router3 = Router()

@router3.message(F.text == "hi")
async def hello_handler(message: Message) -> None:
    """
        Handler for text messages equal to "hi".

        Args:
            message (Message): Incoming message with text "hi".

        Returns:
            None
    """
    await message.answer("Hi!")

@router.callback_query(F.data.startswith("lang_"))
async def lang_callback_handler(callback: CallbackQuery) -> None:
    """
        Handler for callback queries where data starts with "lang_".

        Args:
            callback (CallbackQuery): Incoming callback query.

        Returns:
            None
    """
    await callback.answer("You have chosen a language")