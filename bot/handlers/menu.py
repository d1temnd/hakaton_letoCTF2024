from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from bot import dp, logger, bot, UserStates
import ui, config
import api


@dp.message(Command(commands="start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await bot.set_my_commands(ui.commands)

    if api.auth(message.from_user.id, message.from_user.username):
        logger.info(f"User {message.from_user.id} authorized")
        profile = api.get_profile(message.from_user.id)
        if profile:
            await message.answer(
                ui.TEXT_MENU.format(
                    username=profile["username"],
                    score=profile["score"],
                    position=profile["position"],
                ),
                reply_markup=ui.keyboard_menu,
            )
        else:
            logger.error(f"User {message.from_user.id} not found")
            await message.answer(ui.TEXT_AUTH_FAILED)
    else:
        logger.info(f"User {message.from_user.id} not authorized")
        await message.answer(ui.TEXT_AUTH_FAILED)


@dp.callback_query(lambda c: c.data == "task")
async def process_callback_task(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    task = api.get_task(callback_query.from_user.id)
    if task:
        if task["passed"]:
            await bot.edit_message_text(
                text=ui.TEXT_TASK_PASSED,
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=ui.keyboard_only_back,
            )
        else:
            await bot.edit_message_text(
                text=ui.TEXT_TASK.format(text=task["text"]),
                chat_id=callback_query.from_user.id,
                message_id=callback_query.message.message_id,
                reply_markup=ui.keyboard_task,
            )
    else:
        await bot.edit_message_text(
            text=ui.TEXT_NO_TASK,
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=ui.keyboard_only_back,
        )


@dp.callback_query(lambda c: c.data == "scoreboard")
async def process_callback_scoreboard(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    scoreboard = api.get_scoreboard()
    text_scoreboard = "\n".join(
        [
            f"{i+1}. {user['username']} - {user['score']}"
            for i, user in enumerate(scoreboard)
        ]
    )
    await bot.edit_message_text(
        text=ui.TEXT_SCOREBOARD.format(scoreboard=text_scoreboard),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=ui.keyboard_only_back,
    )


@dp.callback_query(lambda c: c.data == "to_menu")
async def process_callback_go_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    profile = api.get_profile(callback_query.from_user.id)
    await bot.edit_message_text(
        ui.TEXT_MENU.format(
            username=profile["username"],
            score=profile["score"],
            position=profile["position"],
        ),
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=ui.keyboard_menu,
    )
