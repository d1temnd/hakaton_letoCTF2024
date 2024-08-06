from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from bot import dp, logger, bot, UserStates
import ui, config, api


async def broadcast_vote(from_user_id: int):
    users = api.get_users()
    task = api.get_task(from_user_id)
    file_path = await bot.get_file(task["file_id"])
    for user in users:
        if user['task_id'] == task['id']:
            continue
        try:
            await bot.send_photo(user["user_id"], file_path, ui.TEXT_VOTE.format(task=task["text"]))
        except Exception:
            pass
