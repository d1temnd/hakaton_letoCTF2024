from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from bot import dp, logger, bot, UserStates
import ui, config, api


@dp.message(Command(commands="start_game"))
async def start_game(message: types.Message, state: FSMContext):
    if api.start_game():
        await message.answer("Start game")
    else:
        await message.answer("Game not started")
