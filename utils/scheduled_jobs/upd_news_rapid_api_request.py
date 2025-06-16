from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import asyncio
import requests
from decouple import config

from db_peewee.db_news_class import NewsDB, initialize_news_db
from utils.logger_config import logger

def rapid_api_request() -> None:
    """
        Fetch cryptocurrency news data from RapidAPI, filter out existing news by URL,
        parse and save new news items into the database.

        Uses proxy and API key from environment variables.

        Raises:
            requests.RequestException: If the HTTP request to RapidAPI fails.
    """
    initialize_news_db()

    logger.info("Sending a request to RapidAPI")
    url = "https://cryptocurrency-news2.p.rapidapi.com/v1/cryptodaily"
    proxy_url = f"http://{config('proxy')}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }
    headers = {
        "x-rapidapi-key": config('RAPID_KEY'),
        "x-rapidapi-host": "cryptocurrency-news2.p.rapidapi.com",
    }

    try:
        response = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        logger.info("Response received from RapidAPI")

        news_items: List[Dict[str, Any]] = data.get("data", [])
        existing_urls = set(
            row.url for row in NewsDB.select(NewsDB.url)
        )

        today = datetime.now(timezone.utc).date()

        new_news = []
        for item in news_items:
            created_at_str: str = item.get('createdAt', '')
            if not created_at_str:
                continue
            try:
                created_at = datetime.strptime(created_at_str, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError as e:
                logger.error(f"Date parsing error: {created_at_str} — {e}")
                continue

            if created_at.date() != today:
                continue

            news_url: Optional[str] = item.get('url')
            if not news_url or news_url in existing_urls:
                continue

            new_news.append(item)

        logger.info(f"Total number of news received from RapidAPI: {len(news_items)}")
        logger.info(f"New news from RapidAPI to save (today only): {len(new_news)}")

        for item in new_news:
            news_url: Optional[str] = item.get('url')
            title_en: str = item.get('title', '')
            description_en: str = item.get('description', '')
            thumbnail: str = item.get('thumbnail', '')
            created_at_str: str = item.get('createdAt', '')
            logger.info(f"Inserting news: url={news_url}, title_en={title_en}, description_en={description_en}") #test code

            if not news_url:
                logger.warning("Skipping news item with empty URL")
                continue

            if created_at_str:
                try:
                    created_at = datetime.strptime(created_at_str, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError as e:
                    logger.error(f"Date parsing error: {created_at_str} — {e}")
                    created_at = datetime.now()
            else:
                created_at = datetime.now()


            NewsDB.insert(
                url=news_url,
                title_en=title_en,
                description_en=description_en,
                thumbnail=thumbnail,
                createdat=created_at
            ).on_conflict_ignore().execute()

        logger.info("RapidAPI data is saved to the database")

    except requests.RequestException as e:
        logger.error("Error when requesting RapidAPI:", e)

async def rapid_api_request_async():
    await asyncio.to_thread(rapid_api_request)

async def schedule_rapid_update():
    try:
        logger.info("Start updating the news database via RapidAPI")
        await rapid_api_request_async()
        logger.info("The end of updating the news database via RapidAPI")
    except Exception as e:
        logger.error(f"Error updating the news database via RapidAPI: {e}")

rapid_api_request()