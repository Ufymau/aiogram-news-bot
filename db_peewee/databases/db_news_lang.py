import os
from utils.languages import LANGUAGES
from db_peewee.db_news_class import NewsDB  # базовая модель
from peewee import SqliteDatabase
from utils.logger_config import logger


def get_db(lang_code: str) -> SqliteDatabase:
    """
        Creates and returns connection to databases SQlite object for the specified language.

        Args:
            lang_code (str): Lang code, example 'en', 'ru', 'fr'. (check dict in LANGUAGES -> languages.py)

        Return:
            SqliteDatabase: The database object associated with the news_{lang_code}.db file in the 'db_peewee -> databases -> news' folder.
    """
    base_dir = os.path.dirname(__file__)  # папка, где лежит этот скрипт
    target_dir = os.path.join(base_dir, 'news')
    db_name = f"news_{lang_code}.db"
    db_path = os.path.join(target_dir, db_name)
    return SqliteDatabase(db_path)

def create_news_model(lang_code: str):
    """
        Creates NewsDB model Class, linked to the database for the specified language.

        Args:
            lang_code (str): Lang code, example 'en', 'ru', 'fr'. (check dict in LANGUAGES -> languages.py)

        Returns:
            tuple: A tuple from (newsdblang, db), where:

            newsdblang:
            The model class associated with the database.

            db:
            The SQLiteDatabase object for this database.
        """
    db = get_db(lang_code)

    class Newsdblang(NewsDB):
        class Meta:
            database = db
            table_name = 'newsdb'  # имя таблицы одинаковое во всех базах

    return Newsdblang, db

def initialize_all_news_dbs():
    """
        Initializes databases and creates tables for all languages except English ('en').

        For each language from dict in LANGUAGES -> languages.py, except 'en', creates a database and a table 'newsdb',
        if they don't exist yet.

        Logging the successful completion of initialization.
    """
    for lang_code in LANGUAGES.keys():
        if lang_code == 'en':
            continue  # Skip the base language
        NewsDBLang, db = create_news_model(lang_code)
        db.connect()
        db.create_tables([NewsDBLang], safe=True)
        db.close()
    logger.info("Databases for all languages except 'en' and tables are initialized.")

