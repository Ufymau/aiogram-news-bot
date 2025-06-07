import operator
from typing import List, Union, Tuple
from functools import reduce
from datetime import datetime, timedelta
from utils.languages import LINK
from db_peewee.databases.db_news_lang import create_news_model

def get_all_daily(lang_code: str) -> List[str]:
    """
        Retrieve all news items created today for the specified language.

        Args:
            lang_code (str): Language code to select the appropriate news database/model.

        Returns:
            List[str]: List of formatted news strings with description and link.
    """
    news_db_lang, db = create_news_model(lang_code)
    db.connect()

    today = datetime.now().date()
    start_datetime = datetime.combine(today, datetime.min.time())  # начало сегодняшнего дня
    end_datetime = start_datetime + timedelta(days=1)             # начало следующего дня

    query = news_db_lang.select().where(
        (news_db_lang.createdat >= start_datetime) & (news_db_lang.createdat < end_datetime)
    ).order_by(news_db_lang.createdat.desc())

    return set_links(lang_code, query)


def get_key_daily(*keys: Union[str, List[str], Tuple[str, ...]], lang_code: str) -> List[str]:
    """
        Retrieve news items created today that match any of the given keywords in their description,
        for the specified language.

        If a single list or tuple of keys is passed, it will be unpacked.

        Args:
            *keys (Union[str, List[str], Tuple[str, ...]]): Keywords to filter news descriptions.
            lang_code (str): Language code to select the appropriate news database/model.

        Returns:
            List[str]: List of formatted news strings with description and link.
        """
    news_db_lang, db = create_news_model(lang_code)
    db.connect()

    if len(keys) == 1 and isinstance(keys[0], (list, tuple)): # Если передали один аргумент — список ключей, распаковываем
        keys = keys[0]

    today = datetime.now().date()
    start_datetime = datetime.combine(today, datetime.min.time())
    end_datetime = start_datetime + timedelta(days=1)

    conditions = []
    for key in keys: ###key search, but if there are errors, then the key search should be done using the English database, and the answers should be extracted from the language database.
        conditions.append(news_db_lang.description ** f'{key}')        # exact match
        conditions.append(news_db_lang.description ** f'{key} %')      # at the beginning
        conditions.append(news_db_lang.description ** f'% {key} %')    # in the middle
        conditions.append(news_db_lang.description ** f'% {key}')      # at the end

    combined_condition = reduce(operator.or_, conditions)

    query = news_db_lang.select().where(
        (news_db_lang.createdat >= start_datetime) & (news_db_lang.createdat < end_datetime) &
        combined_condition
    ).order_by(news_db_lang.createdat.desc())

    return set_links(lang_code, query)


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
        description = news.description or ""
        url = news.url or ""
        results.append(f"{description} [[{LINK.get(lang_code, 'link')}]({url})]")
    return results
