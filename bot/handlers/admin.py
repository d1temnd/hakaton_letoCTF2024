from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import api
import ui
import config
from bot import bot, dp, logger


# Рассылка сообщений всем пользователям о старте
async def broadcast_start_game():
    users = api.get_users()
    print(users)
    for user in users:
        try:
            await bot.send_message(user["user_id"], ui.TEXT_GAME_STARTED)
        except Exception:
            pass


# Рассылка сообщений всем пользователям о конце игры
async def broadcast_end_game():
    users = api.get_users()
    for user in users:
        try:
            await bot.send_message(user["user_id"], ui.TEXT_GAME_ENDED)
        except Exception:
            pass


# Админка на старт игры
@dp.message(Command(commands="start_game"))
async def start_game(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
    if api.start_game():
        await broadcast_start_game()
    else:
        await message.answer("Game not started")


# Админка на конец игры
@dp.message(Command(commands="end_game"))
async def end_game(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
    if api.end_game():
        await broadcast_end_game()
    else:
        await message.answer("Game not ended")
