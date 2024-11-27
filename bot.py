import asyncio
import logging
import re

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import CommandStart, Command
from config import Config, load_config
from src.handlers import echo


logger = logging.getLogger(__name__)

async def start_command(message: Message):
    await message.answer("Добро пожаловать. Вы активировали бот.")


async def help_command(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - начать взаимодействие\n"
        "/help - справка о командах\n"
        "/settings - настройки бота\n"
        "/summarize - текст видео\n" # нужно ли это сюда?
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


#Функция отправления запроса к серверу для получения текста видео
async def video_summarize(session, url):
    try:
        async with session.post("http://127.0.0.1:5000/summarize", json={"video_url": url}, timeout=10) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    return data.get("summary", "Server didn't return video text")
                except aiohttp.ContentTypeError:
                    logger.error(f"Server returned non-JSON response for URL: {url}")
                    return f"Error: Server returned non-JSON response"
            else:
                logger.error(f"Server returned status code {response.status} for URL: {url}")
                return f"Error: Server returned status code {response.status}"
    except asyncio.TimeoutError:
        logger.error(f"Timeout while fetching video text for URL: {url}")
        return "Error: Request timed out"
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching video text for URL: {url}, Error: {e}")
        return f"Error: {e}"

async def summarize_command(youtube_url):
    youtube_regex = r"^https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}$"
    if not re.match(youtube_regex, youtube_url):
        return "Invalid YouTube URL"

    async with aiohttp.ClientSession() as session:
        result = await video_summarize(session, youtube_url)
        return result        


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
    dp.message.register(summarize_command, Command('summarize')) # нужно ли это сюда?

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
