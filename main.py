import asyncio

from db_peewee.db_users_class import initialize_user_db
from telegram_bot.create_bot import bot, dp, scheduler
from telegram_bot.handlers import routers
from telegram_bot.middlewares.news_middleware import UserLanguageMiddleware
from utils.logger_config import logger
from utils.scheduled_jobs import scheduled_jobs

from utils.scheduled_jobs.translate_to_lang_db import fill_translated_news

"""
At the first launch main, initializes the user database and the news database, 
queries the current available news, translates it into the installed languages, 
and creates a database for each language. 
Only after that, asynchronous operation of the telegram bot will be started.
In the process, it updates the news databases and sends the latest news 
to the user in the language of his choice.
"""
initialize_user_db()
fill_translated_news() #It takes data from the news.db. In English, it translates this data from the database into languages that are supported by the script.(Translates  ~10-15 news items * (*lang), now there are 7 languages.)

async def main() -> None:
    logger.info("Main starting")

    #A list of schedulers performed 2 times a day.
    for func, trigger, job_id, job_name in scheduled_jobs:
        scheduler.add_job(func, trigger, id=job_id, name=job_name)
        logger.info(f"Scheduled job '{job_id}': {job_name}")

    scheduler.start()

    dp.update.middleware(UserLanguageMiddleware())

    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())