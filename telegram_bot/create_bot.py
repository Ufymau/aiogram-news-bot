"""
The initialization module for the bot and related objects.

When importing this module, global objects are created.:

- `bot' is an instance of aiogram. A bot initialized with a token.
- `dp' is an instance of ariogram. Dispatcher with memory for states.
- `scheduler' is an instance of AsyncIOScheduler with the Europe/Moscow timezone.
- `admins' — the list of administrator IDs loaded from the config.

These objects are created synchronously when the module is imported and are ready for use.
"""

from typing import List

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.logger_config import logger

logger.info("Initializing bot parameters")

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins: List[int] = [int(admin_id) for admin_id in config('ADMINS').split(',')]

bot: Bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp: Dispatcher = Dispatcher(storage=MemoryStorage())

