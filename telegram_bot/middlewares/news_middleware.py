from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db_peewee.db_users_class import get_user_language

class UserLanguageMiddleware(BaseMiddleware):
    """
        Middleware to inject the user's language code into the handler's data dictionary.

        This middleware extracts the user ID from the incoming Telegram event,
        retrieves the user's preferred language code from the database,
        and adds it to the `data` dictionary passed to the handler.
        If the user is not found, it defaults to English ("en").

        Attributes:
            None
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
            Middleware call method that enriches handler data with user language.

            Args:
                handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]):
                    The next handler in the middleware chain.
                event (TelegramObject): Incoming Telegram event (message, callback, etc.).
                data (Dict[str, Any]): Data dictionary to pass to the handler.

            Returns:
                Any: The result of the handler execution.
        """
        user = getattr(event, "from_user", None)
        if user:
            user_id = user.id
            lang_code = get_user_language(user_id)
            data["lang_code"] = lang_code
        else:
            data["lang_code"] = "en"
        return await handler(event, data)
