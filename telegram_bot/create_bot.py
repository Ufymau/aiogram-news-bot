from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.logger_config import logger
from typing import List


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins: List[int] = [int(admin_id) for admin_id in config('ADMINS').split(',')]

bot: Bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp: Dispatcher = Dispatcher(storage=MemoryStorage())

logger.info("Bot starting")