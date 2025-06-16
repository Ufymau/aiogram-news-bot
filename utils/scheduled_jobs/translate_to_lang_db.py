from typing import Optional

import asyncio

from db_peewee.db_news_class import NewsDB,news_db
from utils.languages import LANGUAGES
from utils.logger_config import logger
from utils.translator import translate_text

def fill_translated_news() -> None:
    """
    Translates news from English data in database (title_en, description_en) into all languages from LANGUAGES,
    except 'en', and fills the corresponding fields in the database.

    For each news item missing a translation in the target language (where title_{lang_code} is NULL or empty),
    the function uses translate_text to translate and saves the result.

    Exceptions are not suppressed to allow error tracking in logs.

    return: None
    """
    logger.info("Starting translating news.")
    if news_db.is_closed():
        news_db.connect()
    # logger.info("The connection to the news database was opened.")
    try:

        for lang_code in LANGUAGES:
            if lang_code == 'en':
                continue  # Skip English

            title_field: str = f'title_{lang_code}'
            description_field: str = f'description_{lang_code}'

            # Query news where the translation is missing or empty
            query = NewsDB.select().where(
                (getattr(NewsDB, title_field) >> None) | (getattr(NewsDB, title_field) == '')
            )

            logger.info(f"Starting translation to '{lang_code}'. Number of news items to translate: {query.count()}")

            total = query.count()
            last_logged_percent = 0
            for idx, news in enumerate(query, start=1):
                original_title: Optional[str] = getattr(news, 'title_en', None)
                original_description: Optional[str] = getattr(news, 'description_en', None)

                if not original_title and not original_description:
                    logger.debug(f"Skipping news with url={news.url} — no English text available.")
                    continue

                try:
                    translated_title: Optional[str] = translate_text(original_title, lang_code) if original_title else None
                    translated_description: Optional[str] = translate_text(original_description, lang_code) if original_description else None

                    setattr(news, title_field, translated_title)
                    setattr(news, description_field, translated_description)

                    news.save()
                    percent = int((idx / total) * 100)
                    if percent >= last_logged_percent + 1 or idx == total:
                        remaining = total - idx
                        logger.info(f"Translated {idx} ({percent}%), remaining {remaining} news items to '{lang_code}'.")
                        last_logged_percent = percent
                except Exception as e:
                    logger.error(f"Error translating news with url={news.url} to '{lang_code}': {e}")
    finally:
        news_db.close()
        # logger.info("The connection to the news database is closed.")

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
        await fill_translated_news_async()
    except Exception as e:
        logger.error(f"Error async def schedule_translate_update: {e}")

if __name__ == "__main__":
    fill_translated_news()