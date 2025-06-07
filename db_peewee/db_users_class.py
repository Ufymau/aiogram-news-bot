import os
import traceback
from peewee import Model, SqliteDatabase, IntegerField, CharField, BooleanField
from utils.decorators.lang_decorators import print_result_decorator
from utils.logger_config import logger
from typing import Optional


logger.info("Start logging users.db")

base_dir = os.path.dirname(__file__)
db_path  = os.path.join(base_dir, 'databases', 'users.db')
db = SqliteDatabase(db_path )

class UserDB(Model):
    """
        Model for storages user notes.

        Attributes:
            user_id (int): Telegram user id.
            username (str): Telegram username.
            first_name (str): Telegram user first name.
            last_name (str): Telegram user last name.
            language_code (str): Language which user was selected.
            is_bot (bool): Info about User or Bot, if the bot value is True then the value is False.
            news_choice (str): Type of format news, which user was selected (all news or news by keyword).
            news_keywords (Optional[str]): The keywords that the user selected.
    """
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    language_code = CharField(null=True)
    is_bot = BooleanField(default=False)
    news_choice = CharField(null=True)
    news_keywords = CharField(null=True)

    class Meta:
        database = db

def initialize_UserDB() -> None:
    """
        Connects to the database User_DB and creates table, if it doesn't exist.

        Returns:
        None
    """
    try:
        logger.info("Starting UserDB initialization...")
        db.connect()
        db.create_tables([UserDB], safe=True)
        logger.info("UserDB initialization completed (table created or already exists).")
    except Exception as e:
        logger.error(f"Error initializing UserDB: {e}", exc_info=True)
    finally:
        db.close()


def save_user_to_db(user_data: dict) -> None:
    """
    Saves or updates user data in the UserDB database.

    Args:
        user_data (dict): User data from callback Telegram.

    Returns:
        None
    """
    try:
        if db.is_closed():
            db.connect()

        user, created = UserDB.get_or_create(user_id=user_data['user_id'])
        user.username = user_data.get('username')
        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.language_code = user_data.get('language_code')
        user.is_bot = user_data.get('is_bot', False)

        user.save()

        logger.info(f"User {user.user_id} saved to users.db. Created: {created}")

    except Exception as e:
        logger.error(f"Error saving user to users.db: {e}\n{traceback.format_exc()}")

def save_user_choice(user_id: int, choice: str, keywords: str = None) -> None:
    """
    Saves or updates user choice (all news or news by keyword) in the UserDB database.

    Args:
        user_id (int): Telegram user id.
        choice (str): Type of format news, which user was selected (all news or news by keyword).
        keywords (Optional[str]): If choice is news by keyword. The keywords that the user selected.

    Return:
        None
    """
    try:
        if db.is_closed():
            db.connect()

        user, created = UserDB.get_or_create(user_id=user_id)
        user.news_choice = choice

        if choice == "news_keyword" and keywords:
            user.news_keywords = keywords

        user.save()

        logger.info(f"Saved choice '{choice}' for user {user_id} with keywords if is: {keywords} to users.db")

    except Exception as e:
        logger.error(f"Error saving user choice to users.db: {e}")


@print_result_decorator
def get_user_language(user_id: int) -> str:
    """
    Return (str): user language from UserDB.

    Args:
        user_id (int): Telegram user id.

    Returns:
        (str): user language
    """
    try:
        user = UserDB.get(UserDB.user_id == user_id)
        return user.language_code or "en"
    except UserDB.DoesNotExist:
        return "en"


def get_user_news_settings(user_id: int) -> str:
    """
    Return (str): type of format news, which user was selected (all news or news by keyword).

    Args:
        user_id (int): Telegram user id.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing:
            - news_choice (str or None): The type of news format selected by the user ('all news' or 'news_keyword').
            - news_keywords (str or None): The keywords selected by the user if choice is 'news_keyword'.
            None if not set or user does not exist.
    """
    try:
        user = UserDB.get(UserDB.user_id == user_id)
        return user.news_choice, user.news_keywords
    except UserDB.DoesNotExist:
        return None, None


if __name__ == "__main__":
    initialize_UserDB()
