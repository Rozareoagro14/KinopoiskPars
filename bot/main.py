import logging
import re
from aiogram import Bot, Dispatcher, executor, types
import aiohttp
from config import API_TOKEN, KINOPOISK_API_KEY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

MAX_MESSAGE_LENGTH = 4096

async def get_movie_info(movie_id):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": KINOPOISK_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()

async def send_long_message(chat_id, text):
    while text:
        part = text[:MAX_MESSAGE_LENGTH]
        await bot.send_message(chat_id, part)
        text = text[MAX_MESSAGE_LENGTH:]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне полную ссылку на страницу фильма на КиноПоиске.")

@dp.message_handler()
async def extract_id_and_fetch_info(message: types.Message):
    try:
        url = message.text
        movie_id_match = re.search(r'kinopoisk\.ru/film/(\d+)', url)
        if movie_id_match:
            movie_id = movie_id_match.group(1)
            movie_info = await get_movie_info(movie_id)
            await send_long_message(message.chat.id, movie_info)
        else:
            await message.reply("Пожалуйста, отправьте корректную ссылку на страницу КиноПоиска.")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.reply("Произошла ошибка при обработке вашего запроса.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
