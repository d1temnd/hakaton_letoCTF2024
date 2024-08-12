from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

# Кнопки
BUT_BACK = "◀ Назад"
BUT_TASK = "📄 Задание"
BUT_SCOREBOARD = "🏆 Рейтинг"
BUT_PASS_TASK = "✏ Сдать задание"
# Тексты
TEXT_BOT_STARTUP = "✅ Бот запущен!"
TEXT_BOT_SHUTDOWN = "❌ Бот отключен!"
TEXT_MENU = "🖐 Добро пожаловать, {username}\n🎟 Очки: {score}\n🏅 Место: {position}\n📄 Ваша задача вместе с напарником, следуя нашим условиям, запечатлить событие на видео. Отчеты отправляйте сюда"
TEXT_AUTH_FAILED = "❌ Авторизация не пройдена!"
TEXT_TASK = "📄 Ваше задание:\n{text}"
TEXT_NO_TASK = "❌ У вас нету активного задания"
TEXT_SCOREBOARD = "🏆 Рейтинг:\n{scoreboard}"
TEXT_PASS_TASK = "📷 Отправьте видео"
TEXT_TASK_PASSED = "✏ Задание сдано, ожидайте результатов!"
TEXT_VOTE = "📢 {text}\nОцените выполнение задание от 0 до 5"
TEXT_VOTE_SENT = "❤ Спасибо за голос!"
TEXT_GAME_STARTED = "🚩 Игра началась! Проверьте свои задания"
TEXT_GAME_ENDED = "🚩 Игра закончилась! Проверьте свой профиль"

# Команды
commands = [BotCommand(command="start", description="Запустить бота и открыть меню")]

# Клавиатура
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
