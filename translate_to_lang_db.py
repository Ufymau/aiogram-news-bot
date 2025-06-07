import os
import asyncio
from utils.languages import LANGUAGES
from db_peewee.db_news_class import NewsDB
from peewee import SqliteDatabase
from utils.logger_config import logger
from utils.translator import translate_text
from db_peewee.databases.db_news_lang import initialize_all_news_dbs, create_news_model

def fill_translated_news() -> None:
    """
        Initializes databases for all languages except 'en',
        then loads all news from the 'news_en.db' database and fills
        the corresponding language databases with translated news.

        For each news item, checks if it already exists in the target database by URL.
        If not, translates the 'title' and 'description' fields and inserts the record.

        Exceptions are logged to prevent interruption of the process.
    """
    initialize_all_news_dbs()
    base_dir = os.path.dirname(__file__)
    en_db_path = os.path.join(base_dir, 'news', 'news_en.db')
    en_db = SqliteDatabase(en_db_path)

    class NewsDBEn(NewsDB):
        class Meta:
            database = en_db
            table_name = 'newsdb'

    en_db.connect()
    all_news = list(NewsDBEn.select())
    en_db.close()

    for lang_code in LANGUAGES.keys():
        if lang_code == 'en':
            continue

        NewsDBLang, db = create_news_model(lang_code)
        db.connect()

        for news in all_news:
            if NewsDBLang.select().where(NewsDBLang.url == news.url).exists():
                continue

            try:
                title_translated = translate_text(news.title, lang_code)
                description_translated = translate_text(news.description, lang_code)

                NewsDBLang.create(
                    url=news.url,
                    title=title_translated,
                    description=description_translated,
                    thumbnail=news.thumbnail,
                    createdat=news.createdat
                )
                logger.info(f"Added translated news to {lang_code}: {news.url}")
            except Exception as e:
                logger.error(f"Error translating news {news.url} to {lang_code}: {e}")

        db.close()


async def fill_translated_news_async() -> None:
    """
        Asynchronous wrapper for the 'fill_translated_news' function,
        runs it in a separate thread to avoid blocking the main event loop.
    """
    await asyncio.to_thread(fill_translated_news)

async def schedule_translate_update() -> None:
    """
        Asynchronous function to start the news translation update process.
        Logs the start and end of the process, as well as any errors encountered.
    """
    try:
        logger.info("Start updating(translation) the news database via news_en.db")
        await fill_translated_news_async()
        logger.info("The end of (translation) the news database via news_en.db")
    except Exception as e:
        logger.error(f"Error u(translation) the news database via news_en.db: {e}")