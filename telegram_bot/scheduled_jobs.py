from apscheduler.triggers.cron import CronTrigger
from utils.work_time.upd_news_rapid_api_request import schedule_rapid_update
from utils.work_time.auto_send_news import schedule_news_send
from db_peewee.databases.translate_to_lang_db import schedule_translate_update


scheduled_jobs = [
    (
        schedule_rapid_update,
        CronTrigger(hour=5, minute=30),
        "rapid_update_morning",
        "Rapid update at 05:30"
    ),
    (
        schedule_translate_update,
        CronTrigger(hour=5, minute=32),
        "translate_update_morning",
        "Translate update at 05:32"
    ),
    (
        schedule_news_send,
        CronTrigger(hour=6, minute=0),
        "news_send_morning",
        "News send at 06:00"
    ),
    (
        schedule_rapid_update,
        CronTrigger(hour=17, minute=30),
        "rapid_update_evening",
        "Rapid update at 17:30"
    ),
    (
        schedule_translate_update,
        CronTrigger(hour=17, minute=32),
        "translate_update_evening",
        "Translate update at 17:32"
    ),
    (
        schedule_news_send,
        CronTrigger(hour=18, minute=0),
        "news_send_evening",
        "News send at 18:00"
    ),
]
