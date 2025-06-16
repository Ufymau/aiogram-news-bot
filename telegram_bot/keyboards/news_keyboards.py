from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.languages import NEWS_BUTTONS

def news_keyboard(lang_code: str)-> InlineKeyboardMarkup:
    """
        Creates an inline keyboard markup for news options based on the user's language.

        The keyboard contains two buttons:
        - "news_all" for displaying all news,
        - "news_keyword" for news filtered by keywords.

        If the language code is not found in NEWS_BUTTONS, falls back to English buttons.

        Args:
            lang_code (str): Language code to select the appropriate button texts.

        Returns:
            InlineKeyboardMarkup: Inline keyboard with news option buttons arranged one per row.
    """
    builder = InlineKeyboardBuilder()
    buttons: List[str] = NEWS_BUTTONS.get(lang_code, NEWS_BUTTONS["en"])  # fallback to English
    builder.button(text=buttons[0], callback_data="news_all")
    builder.button(text=buttons[1], callback_data="news_keyword")
    builder.adjust(1)  # 1 button per row; can be changed to 2 for two buttons per row
    return builder.as_markup()