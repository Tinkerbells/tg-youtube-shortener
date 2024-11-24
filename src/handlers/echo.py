import re
from aiogram import Router
from aiogram.types import Message


router: Router = Router()

YOUTUBE_REGEX = re.compile(
    r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=[\w-]+|[\w-]+|playlist\?list=[\w-]+)'
)


@router.message()
async def process_any_message(message: Message):
    if match := YOUTUBE_REGEX.search(message.text):
        youtube_link = match.group(0)
        await message.answer(f"Я нашёл YouTube ссылку: {youtube_link}")
    else:
        await message.answer("В вашем сообщении нет YouTube ссылки.")
