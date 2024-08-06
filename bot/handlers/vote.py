from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import api
import ui
from bot import bot, logger, router


# Рассылка голосования
async def broadcast_vote(from_user_id: int):
    users = api.get_users()
    task = api.get_task(from_user_id)
    file_id = task["file_id"]

    buttons = []
    for i in range(5):
        buttons.append(
            InlineKeyboardButton(
                text=str(i + 1), callback_data=f'vote_{task["id"]}_{str(i + 1)}'
            )
        )
    keyboard_vote = InlineKeyboardMarkup(inline_keyboard=[buttons])

    for user in users:
        if user["task_id"] == task["id"]:
            continue
        try:
            print(user)
            await bot.send_video(user["user_id"], file_id, duration=10)
            await bot.send_message(
                user["user_id"],
                ui.TEXT_VOTE.format(text=task["text"]),
                reply_markup=keyboard_vote,
            )
        except Exception:
            pass

    logger.debug(f"Broadcasted vote for task {task['id']}")


# Обработчик нажатия на кнопку голосования
@router.callback_query(lambda c: c.data.startswith("vote"))
async def process_callback_send_vote(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    _, task_id, vote = callback_query.data.split("_")
    api.send_vote(callback_query.from_user.id, task_id, vote)
    await bot.edit_message_text(
        text=ui.TEXT_VOTE_SENT,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )
    logger.debug(
        f"User {callback_query.from_user.id} voted for task {task_id} with {vote}"
    )
