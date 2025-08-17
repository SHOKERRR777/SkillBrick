import logging

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import TOKEN, ADMINS_ID

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Инициирование бота + настраиваем parse_mode как HTML по-умолчанию
dp = Dispatcher()
router = Router()

admins = [int(admins) for admins in ADMINS_ID] # Хранение айди админов

# Настраиваем логирование для отдельного использования в нужных местах
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)