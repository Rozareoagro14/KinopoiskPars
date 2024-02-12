import json
from aiogram import types

async def send_movie_info(message: types.Message, data):
    # Отправка информации о фильме по отдельным пунктам
    await message.answer(f"Название: {data.get('name', 'Название не указано')}")
    await message.answer(f"Год: {data.get('year', 'Год не указан')}")
    await message.answer(f"Рейтинг КиноПоиска: {data.get('rating', {}).get('kp', 'Нет рейтинга')}")
    await message.answer(f"Краткое описание: {data.get('description', 'Описание отсутствует').split('.')[0] + '.'}")
    await message.answer(f"Полное описание: {data.get('description', 'Описание отсутствует')}")

    genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
    await message.answer(f"Жанр: {genres}")

    # Обработка информации о режиссёрах
    directors = ', '.join([person['name'] for person in data.get('persons', []) if person.get('profession') == 'режиссеры'])
    if directors:
        await message.answer(f"Режиссёр(ы): {directors}")
    else:
        await message.answer("Режиссёры не указаны.")

    # Обработка информации об актёрах и их ролях
    actors_info = []
    for person in data.get('persons', []):
        if person.get('profession') == 'актеры':
            actor_name = person.get('name', 'Не указано')
            role = person.get('description', 'Роль не указана')
            actors_info.append(f"{actor_name} ({role})")

    actors_str = ', '.join(actors_info[:5])  # Ограничиваем вывод первыми пятью актёрами
    if actors_str:
        await message.answer(f"Актерский состав: {actors_str}")
    else:
        await message.answer("Актерский состав не указан.")

    if data.get('poster', {}).get('url'):
        await message.answer_photo(data['poster']['url'])

async def save_data(data):
    # Сохранение данных в файл
    with open('D:\\Bots\\kinopoisktest\\Meta.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
