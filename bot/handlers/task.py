from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from bot import dp, logger, bot, UserStates
import ui, config, api
from handlers.vote import broadcast_vote


@dp.callback_query(lambda c: c.data == "pass_task")
async def process_callback_pass_task(
    callback_query: types.CallbackQuery, state: FSMContext
):
    await bot.answer_callback_query(callback_query.id)
    await state.set_state(UserStates.pass_task)
    profile = api.get_profile(callback_query.from_user.id)
    await state.set_data({"task_id": profile["task_id"]})
    await bot.edit_message_text(
        text=ui.TEXT_PASS_TASK,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
    )


@dp.message(StateFilter(UserStates.pass_task), F.photo)
async def handle_photo(message: types.Message, state: UserStates):
    photo = message.photo[-1]
    file_id = photo.file_id
    task_id = (await state.get_data())["task_id"]
    api.pass_task(message.from_user.id, task_id, file_id)

    await broadcast_vote(message.from_user.id)

    await message.answer(ui.TEXT_TASK_PASSED, reply_markup=ui.keyboard_only_back)
    await state.clear()


@dp.message(StateFilter(UserStates.pass_task), F.video)
async def handle_video(message: types.Message, state: UserStates):
    video = message.video
    file_id = video.file_id
    task_id = (await state.get_data())["task_id"]
    api.pass_task(message.from_user.id, task_id, file_id)

    await broadcast_vote(message.from_user.id)

    await message.answer(ui.TEXT_TASK_PASSED, reply_markup=ui.keyboard_only_back)
    await state.clear()