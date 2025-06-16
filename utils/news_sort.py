from datetime import datetime, timedelta
from functools import reduce
import operator
from typing import List, Union, Tuple

from db_peewee.db_news_class import NewsDB, news_db
from utils.languages import LINK
from utils.logger_config import logger

def get_all_daily(lang_code: str) -> List[str]:
    """
    Retrieve all news descriptions created today for the specified language,
    along with their URLs.

    Args:
        lang_code (str): Language code, e.g. 'en', 'ru', 'fr'.

    Returns:
        List[str]: List of formatted strings with description and link.
    """
    if news_db.is_closed():
        news_db.connect()

    try:
        today = datetime.now().date()
        start_datetime = datetime.combine(today, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)

        description_field = getattr(NewsDB, f'description_{lang_code}')


        query = (NewsDB
                 .select()
                 .where(
                    (NewsDB.createdat >= start_datetime) &
                    (NewsDB.createdat < end_datetime) &
                    (description_field.is_null(False))
                 )
                 .order_by(NewsDB.createdat.desc())
                )


    finally:
        if not news_db.is_closed():
            news_db.close()

    return set_links(lang_code=lang_code, query=query)

def get_key_daily(*keys: Union[str, List[str], Tuple[str, ...]], lang_code: str) -> List[str]:
    if news_db.is_closed():
        news_db.connect()

    if len(keys) == 1 and isinstance(keys[0], (list, tuple)):
        keys = keys[0]

    if not keys:
        if not news_db.is_closed():
            news_db.close()
        return []

    today = datetime.now().date()
    start_datetime = datetime.combine(today, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)

    description_en_field = getattr(NewsDB, 'description_en')

    conditions = []
    for key in keys:
        key = key.strip()
        if not key:
            continue
        conditions.append(description_en_field ** f'{key}')
        conditions.append(description_en_field ** f'{key} %')
        conditions.append(description_en_field ** f'% {key} %')
        conditions.append(description_en_field ** f'% {key}')

    if not conditions:
        if not news_db.is_closed():
            news_db.close()
        return []

    combined_condition = reduce(operator.or_, conditions)

    query = (NewsDB
             .select()
             .where(
                 (NewsDB.createdat >= start_datetime) &
                 (NewsDB.createdat < end_datetime) &
                 combined_condition
             )
             .order_by(NewsDB.createdat.desc())
            )

    logger.info(f"Found {query.count()} news matching keys {keys} in English description.")

    if not news_db.is_closed():
        news_db.close()

    return set_links(lang_code=lang_code, query=query)

def set_links(lang_code: str, query) -> List[str]:
    """
        Format query results by appending a localized link to each news description.

        Args:
            lang_code (str): Language code to select the appropriate link text.
            query: Peewee query result iterable containing news items.

        Returns:
            List[str]: List of formatted news strings with description and localized link.
    """
    results = []
    for news in query:
        description = getattr(news, f'description_{lang_code}', '') or ''
        url = news.url or ""
        results.append(f"{description} [[{LINK.get(lang_code, 'link')}]({url})]")
    return results