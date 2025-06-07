import asyncio
from telegram_bot.create_bot import bot, dp, scheduler
from telegram_bot.handlers import routers
from telegram_bot.middlewares.news_middleware import UserLanguageMiddleware
from utils.logger_config import logger
from db_peewee.db_users_class import initialize_UserDB
from db_peewee.db_news_class import initialize_NewsDB
from telegram_bot.scheduled_jobs import scheduled_jobs
from utils.work_time.upd_news_rapid_api_request import rapid_api_request
from db_peewee.databases.translate_to_lang_db import fill_translated_news

"""
At the first launch main, initializes the user database and the news database, 
queries the current available news, translates it into the installed languages, 
and creates a database for each language. 
Only after that, asynchronous operation of the telegram bot will be started.
In the process, he updates the news databases and sends the latest news 
to the user in the language of his choice.
"""
initialize_UserDB() #initialize UserDB.
rapid_api_request() #initialize NewsDB_en and fills it with data. (Receives 200 news items.)
fill_translated_news() #It takes data from NewsDB_en, and uses a translator to fill in the NewsDB_*lang. Receives 200 news items.(Translates  200 news items * (*lang), now there are 7 languages.) [~The first time it takes 40 minutes...].

async def main() -> None:
    logger.info("Main stating")

    #A list of schedulers performed 2 times a day.
    for func, trigger, job_id, job_name in scheduled_jobs:
        scheduler.add_job(func, trigger, id=job_id, name=job_name)
        logger.info(f"Scheduled job '{job_id}': {job_name}")

    scheduler.start()

    dp.update.middleware(UserLanguageMiddleware())

    #
    for router in routers:
        dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())