from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.languages import LANGUAGES

def language_keyboard() -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard markup with language buttons.

        Each button displays the language name and has callback data in the format "lang_{code}".

        Returns:
            InlineKeyboardMarkup: Inline keyboard with language selection buttons arranged in 2 columns.
        """
    builder = InlineKeyboardBuilder()
    for code, name in LANGUAGES.items():
        builder.button(text=name, callback_data=f"lang_{code}")
    builder.adjust(2)  # 2 colums
    return builder.as_markup()
