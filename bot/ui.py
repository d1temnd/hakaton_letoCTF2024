from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

# Кнопки
BUT_BACK = "◀ Назад"
BUT_TASK = "📄 Задание"
BUT_SCOREBOARD = "🏆 Рейтинг"
BUT_PASS_TASK = "✏ Сдать задание"
# Тексты
TEXT_BOT_STARTUP = "✅ Бот запущен!"
TEXT_BOT_SHUTDOWN = "❌ Бот отключен!"
TEXT_MENU = "🖐 Добро пожаловать в игру, {username}\n🎟 Очки: {score}\n🏅 Место: {position}"
TEXT_AUTH_FAILED = "❌ Авторизация не пройдена!"
TEXT_TASK = "📄 Ваше задание:\n{text}"
TEXT_NO_TASK = "❌ У вас нету задания"
TEXT_SCOREBOARD = "🏆 Рейтинг:\n{scoreboard}"
TEXT_PASS_TASK = "📷 Отправьте фотографию"
TEXT_TASK_PASSED = "✏ Задание сдано, ожидайте результатов!"
TEXT_VOTE = "📢 Оцените выполнение задание от 0 до 5\n{text}"

# Команды
commands = [BotCommand(command="start", description="Запустить бота и открыть меню")]

keyboard_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUT_TASK, callback_data="task"),
            InlineKeyboardButton(text=BUT_SCOREBOARD, callback_data="scoreboard"),
        ]
    ]
)

keyboard_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUT_BACK, callback_data="to_menu"),
            InlineKeyboardButton(text=BUT_PASS_TASK, callback_data="pass_task"),
        ]
    ]
)

keyboard_only_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUT_BACK, callback_data="to_menu"),
        ]
    ]
)

keyboard_vote = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="0", callback_data="vote_0"),
            InlineKeyboardButton(text="1", callback_data="vote_1"),
            InlineKeyboardButton(text="2", callback_data="vote_2"),
            InlineKeyboardButton(text="3", callback_data="vote_3"),
            InlineKeyboardButton(text="4", callback_data="vote_4"),
            InlineKeyboardButton(text="5", callback_data="vote_5"),
        ]
    ]
)
