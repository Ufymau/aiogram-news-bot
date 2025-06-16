from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class InlineKeyboardManager:
    def __init__(self, buttons: Dict[str, str], buttons_per_row: int = 2) -> None:
        """
        Initialize the InlineKeyboardManager.

        Args:
            buttons (Dict[str, str]): A dictionary mapping button text to callback data.
            buttons_per_row (int, optional): Number of buttons per row. Defaults to 2.
        """
        self.buttons: Dict[str, str] = buttons
        self.buttons_per_row : int = buttons_per_row
        self.builder = InlineKeyboardBuilder()
        self._build_keyboard()

    def _build_keyboard(self) -> None:
        """
            Build the inline keyboard by adding buttons from the buttons dictionary
            and adjusting the layout according to buttons_per_row.
        """
        for text, callback_data in self.buttons.items():
            self.builder.button(text=text, callback_data=callback_data)
        self.builder.adjust(self.buttons_per_row)

    def get_keyboard(self) -> InlineKeyboardMarkup:
        """
            Get the constructed inline keyboard markup.

            Returns:
                InlineKeyboardMarkup: The inline keyboard ready to be sent in a message.
        """
        return self.builder.as_markup()


