import aiogram
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton
from os import environ
from aiogram.utils.token import TokenValidationError
import logging
from dotenv import load_dotenv

load_dotenv()

import aiogram.utils
print(environ.get("TGBotDownloader"))
try:
    bot = Bot(token=environ.get("TGBotDownloader"))
except TokenValidationError as e:
    logging.error("Неверный токен")
    exit(1)
except Exception as e:
    logging.error(e)
    exit(1)

dp = Dispatcher(bot=bot)

@dp.message()
async def youtube_search(message: Message):
    if not message.text.startswith("https://www.youtu"):
        await message.answer("Введите ссылку на видео из YouTube!")
        return
    process = asyncio.create_subprocess_exec("yt-dlp", "-f bestvideo[ext=mp4]+bestaudio[ext=m4a]", "--skip-download", "--abort-on-error", message.text)