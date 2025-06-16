"""
The scheduled_jobs package contains tasks for the APScheduler scheduler.

Main modules:
- auto_send_news: functions for automatically sending news
- translate_to_lang_db: functions for updating translations
- upd_news_rapid_api_request: features for quick news updates

This package defines a scheduled_jobs list containing scheduled jobs for the scheduler.
"""

from typing import Callable, List, Tuple

from apscheduler.triggers.cron import CronTrigger

from utils.scheduled_jobs.auto_send_news import schedule_news_send
from utils.scheduled_jobs.translate_to_lang_db import schedule_translate_update
from utils.scheduled_jobs.upd_news_rapid_api_request import schedule_rapid_update


scheduled_jobs: List[Tuple[Callable, CronTrigger, str, str]] = [
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
        CronTrigger(hour=20, minute=3),
        "news_send_evening",
        "News send at 18:00"
    ),
]