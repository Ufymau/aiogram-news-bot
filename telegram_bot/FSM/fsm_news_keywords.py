from aiogram.filters.state import State, StatesGroup

class NewsKeywordStates(StatesGroup):
    """
        State group for managing the news keyword input process in a finite state machine (FSM).

        Attributes:
            waiting_for_keywords (State): State indicating that the bot is waiting for the user to input keywords.
    """
    waiting_for_keywords = State()


