import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
import asyncio

import config
import ui

# Логирование
logger = logging.getLogger()
# filehandler = RotatingFileHandler(
#     "bot.log", mode="w", maxBytes=1024 * 1024 * 10, backupCount=2
# )
# filehandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
# logger.setLevel(logging.DEBUG)
# logger.addHandler(filehandler)

# Хранилище состояний
storage = MemoryStorage()

# Бот токен
bot = Bot(token=config.TELEGRAM_TOKEN)

# Диспетчер для бота
dp = Dispatcher(bot=bot, storage=storage)


class UserStates(StatesGroup):
    pass_task = State()


# При включении
async def on_startup():
    logger.debug("Bot started!")

    await bot.send_message(chat_id=config.ADMIN_ID, text=ui.TEXT_BOT_STARTUP)


# При отключении
async def on_shutdown():
    logger.debug("Bot shutdown!")

    await bot.send_message(chat_id=config.ADMIN_ID, text=ui.TEXT_BOT_SHUTDOWN)


def start_bot():  # Запуск бота
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    asyncio.run(dp.start_polling(bot, skip_updates=True))


if __name__ == "__main__":
    start_bot()
