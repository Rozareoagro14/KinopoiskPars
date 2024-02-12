import logging
import re
import aiohttp
import json
from aiogram import Bot, types, Router, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import CommandStart
from config import API_TOKEN, KINOPOISK_API_KEY
from utilities import send_movie_info, save_data


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
router = Router()
dispatcher = Dispatcher(storage=storage)
dispatcher.include_router(router)

async def get_movie_info(movie_id):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}?token={KINOPOISK_API_KEY}"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data

@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне полную ссылку на страницу фильма на КиноПоиске.")

@router.message()
async def extract_id_and_fetch_info(message: types.Message):
    try:
        url = message.text
        movie_id_match = re.search(r'kinopoisk\.ru/film/(\d+)', url)
        if movie_id_match:
            movie_id = movie_id_match.group(1)
            movie_data = await get_movie_info(movie_id)
            await save_data(movie_data)
            await send_movie_info(message, movie_data)
        else:
            await message.answer("Пожалуйста, отправьте корректную ссылку на страницу КиноПоиска.")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")

async def main():
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
