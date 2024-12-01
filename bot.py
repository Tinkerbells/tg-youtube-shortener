import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from future.backports.http.client import responses

from config import Config, load_config
from src.handlers import echo


logger = logging.getLogger(__name__)

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="English", callback_data="lang_en")
        ]
    ]
)

user_language = {}

async def start_command(message: Message):
    await message.answer("Добро пожаловать! Бот активирован")


async def help_command(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - начать взаимодействие\n"
        "/help - справка о командах\n"
        "/settings - настройки бота (выбор языка)\n"
        "Отправьте сообщение с ссылкой, и я предоставлю краткий анализ видео"
    )
    await message.answer(help_text)


async def settings_command(message: Message):
    await message.answer("Выберите язык:", reply_markup=language_keyboard)



async def language_handler(callback: CallbackQuery):
    response = ""
    if callback.data == "lang_ru":
        user_language[callback.from_user.id] = "ru"
        response = "Выбранный язык: Русский 🇷🇺"
    elif callback.data == "lang_en":
        user_language[callback.from_user.id] = "en"
        response = "Chosen Language: English 🇬🇧"
    await callback.message.edit_text(text=response)
    await callback.answer()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()
    dp.include_router(echo.router)

    dp.message.register(start_command, CommandStart())
    dp.message.register(help_command, Command('help'))
    dp.message.register(settings_command, Command('settings'))
    dp.callback_query.register(language_handler)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
