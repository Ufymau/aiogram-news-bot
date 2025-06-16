from peewee import Model, CharField, DateTimeField, SqliteDatabase

from db_peewee.init_database import init_database
from utils.languages import LANGUAGES
from utils.logger_config import logger

news_db = init_database('news.db')

fields = {
    'url': CharField(unique=True),
    'thumbnail': CharField(null=True),
    'createdat': DateTimeField(),
}

for lang in LANGUAGES:
    fields[f'title_{lang}'] = CharField(null=True)
    fields[f'description_{lang}'] = CharField(null=True)

NewsDB = type('NewsDB', (Model,), {
    **fields,
    'Meta': type('Meta', (), {'database': news_db})
})


def initialize_news_db( ) -> None:
    """
        Connects to the database news.db and creates table, if it doesn't exist.
    """
    try:
        if news_db.is_closed():
            logger.info("Connecting to news.db")
            news_db.connect()
        else:
            logger.info("Already connected to news.db")

        tables = news_db.get_tables()
        if NewsDB._meta.table_name not in tables: # type: ignore
            logger.info("Table does not exist, creating tables...")
            news_db.create_tables([NewsDB], safe=True)
            logger.info("Tables created successfully")
        else:
            logger.info("Tables already exist, skipping creation")

    except Exception as e:
        logger.error(f"Exception in function 'initialize_news_db': {e}", exc_info=True)
    finally:
        if not news_db.is_closed():
            news_db.close()
            logger.info("Connection to news.db closed")

if __name__ == "__main__":
    initialize_news_db()