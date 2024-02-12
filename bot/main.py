import logging  # Импорт модуля для логирования
import re  # Импорт модуля для работы с регулярными выражениями
import aiohttp  # Импорт модуля для асинхронных HTTP запросов
import json  # Импорт модуля для работы с JSON
from aiogram import Bot, types, Router, Dispatcher  # Импорт классов из библиотеки aiogram
from aiogram.fsm.storage.memory import MemoryStorage  # Импорт класса для хранения состояний FSM
from aiogram.filters.command import CommandStart  # Импорт фильтра для обработки команды /start
from config import API_TOKEN, KINOPOISK_API_KEY  # Импорт API токенов из файла конфигурации
from utilities import send_movie_info, save_data  # Импорт пользовательских функций

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и хранилища состояний
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()

# Инициализация роутера и диспетчера
router = Router()
dispatcher = Dispatcher(storage=storage)
dispatcher.include_router(router)  # Включение роутера в диспетчер

# Асинхронная функция для получения информации о фильме по его ID
async def get_movie_info(movie_id):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{movie_id}?token={KINOPOISK_API_KEY}"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data

# Обработчик команды /start
@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне полную ссылку на страницу фильма на КиноПоиске.")

# Обработчик всех остальных сообщений
@router.message()
async def extract_id_and_fetch_info(message: types.Message):
    try:
        url = message.text
        # Извлечение ID фильма из URL с помощью регулярного выражения
        movie_id_match = re.search(r'kinopoisk\.ru/(?:film|series)/(\d+)', url)
        if movie_id_match:
            movie_id = movie_id_match.group(1)
            # Получение информации о фильме и отправка её пользователю
            movie_data = await get_movie_info(movie_id)
            await save_data(movie_data)  # Сохранение данных в файл
            await send_movie_info(message, movie_data)  # Отправка информации о фильме
        else:
            await message.answer("Пожалуйста, отправьте корректную ссылку на страницу КиноПоиска.")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса.")

# Асинхронная функция для запуска бота
async def main():
    await dispatcher.start_polling(bot)  # Запуск бота в режиме опроса сообщений

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())  # Запуск асинхронной функции main()
