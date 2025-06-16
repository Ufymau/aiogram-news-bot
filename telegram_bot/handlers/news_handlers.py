from typing import List, Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import asyncio

from db_peewee.db_users_class import get_user_language
from db_peewee.db_users_class import save_user_choice
from telegram_bot.FSM.fsm_news_keywords import NewsKeywordStates
from telegram_bot.keyboards.news_keyboards import news_keyboard
from utils.data_sort import split_messages
from utils.languages import NEWS_QUESTION, ENTER_KEYWORDS_PROMPT, EMPTY_INPUT_RETRY, NO_FRESH_NEWS
from utils.logger_config import logger
from utils.news_sort import get_all_daily, get_key_daily

news_choose_router = Router()

@news_choose_router.callback_query(F.data.startswith("lang_"))
async def choose_news(callback: CallbackQuery) -> None:
    """
        Handler for language selection callback queries starting with "lang_".
        Retrieves the user's language from the database and sends a localized news question
        with a keyboard for further interaction.

        Args:
            callback (CallbackQuery): The callback query object from the user.

        Returns:
            None
    """
    logger.info("Handler choose_news called")

    await asyncio.sleep(1)

    user_id = callback.from_user.id
    lang_code = get_user_language(user_id)
    question = NEWS_QUESTION.get(lang_code, NEWS_QUESTION["en"])
    await callback.message.answer(
        question,
        reply_markup=news_keyboard(lang_code)
    )
    await callback.answer()


news_all_router = Router()

@news_all_router.callback_query(F.data == "news_all")
async def news_all(callback: CallbackQuery, lang_code: Optional[str] = None) -> None:
    """
        Handler for callback query with data "news_all".
        Processes the 'news_all' command, sends the user all the news in his language.

        Args:
            callback (CallbackQuery): The callback query object from the user.
            lang_code (Optional[str]): Optional language code; if not provided, fetched from DB.

        Returns:
            None
    """
    user_id = callback.from_user.id
    lang_code = get_user_language(user_id)

    save_user_choice(user_id, "news_all")
    news_messages: List[str] = get_all_daily(lang_code=lang_code)

    await send_news(callback.message, news_messages, lang_code)

    await callback.answer()

@news_all_router.message(Command(commands=["news_all"]))
async def all_news_command(message: Message) -> None:
    """
        Processes the /news_all command, sends the user all the news in his language.

        Args:
            message (Message): The message object from the user.

        Returns:
            None
    """
    user_id = message.from_user.id
    lang_code = get_user_language(user_id)

    save_user_choice(user_id, "news_all")
    news_messages: List[str] = get_all_daily(lang_code=lang_code)

    await send_news(message, news_messages, lang_code)



news_keyword_router = Router()

@news_keyword_router.callback_query(F.data == "news_keyword")
async def ask_keywords(callback: CallbackQuery, state: FSMContext) -> None:
    """
        Handler for callback query with data "news_keyword".
        Prompts the user to enter keywords for news filtering and sets FSM state.

        Args:
            callback (CallbackQuery): The callback query object from the user.
            state (FSMContext): FSM context to manage user state.

        Returns:
            None
    """
    user_id = callback.from_user.id
    lang_code = get_user_language(user_id)
    await callback.message.answer(f"{ENTER_KEYWORDS_PROMPT.get(lang_code)}")
    await state.set_state(NewsKeywordStates.waiting_for_keywords)
    await callback.answer()

@news_keyword_router.message(Command(commands=["news_keyword"]))
async def key_words_command(message: Message, state: FSMContext) -> None:
    """
        Processes the command to enter keywords.
        Sends the user an invitation to enter keywords and puts the FSM in the standby state.

        Args:
            message (Message): The message object from the user.
            state (FSMContext): The context of the state machine for the current user.

        Returns:
            None
    """
    user_id = message.from_user.id
    lang_code = get_user_language(user_id)

    await message.answer(ENTER_KEYWORDS_PROMPT.get(lang_code))
    await state.set_state(NewsKeywordStates.waiting_for_keywords)


@news_keyword_router.message(NewsKeywordStates.waiting_for_keywords)
async def process_keywords(message: Message, state: FSMContext) -> None:
    """
        Handler for processing user-entered keywords while in the waiting_for_keywords FSM state.
        Validates input, saves user choice, fetches news filtered by keywords,
        translates and sends the news, or informs if no fresh news is found.

        Args:
            message (Message): Incoming message with keywords.
            state (FSMContext): FSM context to manage user state.

        Returns:
            None
        """
    user_id = message.from_user.id
    lang_code = get_user_language(user_id)

    keys: List[str] = [k.strip() for k in message.text.split(",") if k.strip()]
    if not keys:
        await message.answer(f"{EMPTY_INPUT_RETRY.get(lang_code)}")
        return

    save_user_choice(user_id, "news_keyword", keywords=",".join(keys))

    news_messages: List[str] = get_key_daily(*keys, lang_code=lang_code)

    await send_news(message, news_messages, lang_code)

    await state.clear()

async def send_news(
    answer_target: Message,
    news_messages: List[str],
    lang_code: str
                    ) -> None:
    """
        Sends the news to the user, breaking them down into convenient parts.
        If there is no news, it sends a message about their absence.

        Args:
            answer_target (Message): The object of the message to which the text will be sent in response.
            news_messages (List[str]): A list of news messages to send.
            lang_code (str): The language code for message localization.

        Returns:
            None
    """
    if not news_messages:
        await answer_target.answer(f"{NO_FRESH_NEWS.get(lang_code)}")
        return

    messages: List[str] = split_messages(news_messages)
    for msg in messages:
        await answer_target.answer(msg, parse_mode="Markdown")
