import re
from aiogram import Router
from aiogram.types import Message
from bot import summarize_command


router: Router = Router()

YOUTUBE_REGEX = re.compile(
    r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=[\w-]+|[\w-]+|playlist\?list=[\w-]+)'
)

def is_valid_youtube_url(url):
    youtube_regex = r"^https://www\.youtube\.com/watch\?v=[a-zA-Z0-9_-]{11}$"
    return bool(re.match(youtube_regex, url))


# Сюда ли это писать, или в бот или в отдельный файл?
# Дописала часть Ксюши, возможно стоит вынести отельно часть summarize
@router.message()
async def process_any_message(message: Message):
    text = message.text
    if match := YOUTUBE_REGEX.search(text):
        youtube_url = match.group(0)
        if youtube_url and is_valid_youtube_url(youtube_url):
            try:
                video_text = await summarize_command(youtube_url)
                await message.reply(video_text)
            except Exception as e:
                await message.reply(f"Error processing YouTube link: {e}")
        elif youtube_url:
            await message.reply("Invalid YouTube URL")
        else:
            await message.reply("I don't understand this message.")
    else:
        await message.answer("В вашем сообщении нет YouTube ссылки.")



