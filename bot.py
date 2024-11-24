import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart, Command
from config import Config, load_config
from src.handlers import echo


logger = logging.getLogger(__name__)


async def start_command(message: Message):
    await message.answer("Hello!")


async def help_command(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - начать взаимодействие\n"
        "/help - справка о командах\n"
        "/settings - настройки бота\n"
        "Отправьте сообщение, и я распознаю его содержимое."
    )
    await message.answer(help_text)


async def settings_command(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="English", callback_data="lang_en")
            ]
        ]
    )
    await message.answer("Выберите язык:", reply_markup=keyboard)


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

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
