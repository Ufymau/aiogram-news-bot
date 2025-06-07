import asyncio
import requests

from decouple import config
from typing import Any, Dict, List, Optional
from datetime import datetime
from db_peewee.db_news_class import NewsDB
from utils.logger_config import logger
from db_peewee.db_news_class import initialize_NewsDB


logger.info("Start logging Rapid_API requests")

def rapid_api_request() -> None:
    """
        Fetch cryptocurrency news data from RapidAPI, filter out existing news by URL,
        parse and save new news items into the database.

        Uses proxy and API key from environment variables.

        Raises:
            requests.RequestException: If the HTTP request to RapidAPI fails.
    """
    initialize_NewsDB()
    url = "https://cryptocurrency-news2.p.rapidapi.com/v1/cryptodaily"  # API новостной сводки
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
        logger.info("Response received from Rapid_API")

        news_items: List[Dict[str, Any]] = data.get("data", [])
        existing_urls = set(
            row.url for row in NewsDB.select(NewsDB.url)
        )
        new_news = [item for item in news_items if item.get('url') not in existing_urls]
        logger.info(f"Total news from RAPID_API: {len(news_items)}")
        logger.info(f"New news from RAPID_API to save: {len(new_news)}")

        for item in news_items:
            news_url: Optional[str] = item.get('url')
            title: str = item.get('title', '')
            description: str = item.get('description', '')
            thumbnail: str = item.get('thumbnail', '')
            created_at_str: str = item.get('createdAt', '')

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
                title=title,
                description=description,
                thumbnail=thumbnail,
                createdat=created_at
            ).on_conflict_ignore().execute()

        logger.info("Rapid_API data is saved to the database")

    except requests.RequestException as e:
        logger.error("Error when requesting Rapid_API:", e)

async def rapid_api_request_async():
    await asyncio.to_thread(rapid_api_request)

async def schedule_rapid_update():
    try:
        logger.info("Start updating the news database via Rapid_API")
        await rapid_api_request_async()
        logger.info("The end of updating the news database via Rapid_API")
    except Exception as e:
        logger.error(f"Error updating the news database via Rapid_API: {e}")

