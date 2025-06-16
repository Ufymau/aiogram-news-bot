from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from utils.logger_config import logger

class CallSecondRouterMiddleware(BaseMiddleware):
    """
        Middleware that calls a secondary handler after the primary handler for a CallbackQuery event.

        This middleware executes the main handler first, then calls the provided secondary handler.
        Any exceptions raised by the secondary handler are caught and logged without interrupting the flow.

        Attributes:
            second_handler (Callable[[CallbackQuery], Awaitable[Any]]):
                An async function to be called after the main handler, receiving the CallbackQuery event.
    """
    def __init__(self, second_handler: Callable[[CallbackQuery], Awaitable[Any]]) -> None:
        """
            Initialize the middleware with a secondary handler.

            Args:
                second_handler (Callable[[CallbackQuery], Awaitable[Any]]):
                    Async function to call after the main handler.
        """
        super().__init__()
        self.second_handler = second_handler

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:

        """
            Middleware call method that wraps the handler execution.

            Args:
                handler (Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]]):
                    The main handler to execute.
                event (CallbackQuery): The incoming callback query event.
                data (Dict[str, Any]): Additional data passed to the handler.

            Returns:
                Any: The result of the main handler execution.
        """
        # Execute the main handler
        result = await handler(event, data)
        # Call the secondary handler, catching and logging exceptions
        try:
            await self.second_handler(event)
        except Exception as e:
            logger.error(f"Error in second handler called from middleware: {e}")

        return result