# bot/utils.py

def format_movie_data(data):
    # Пример функции, форматирующей данные о фильме для отправки пользователю
    # Весь код внутри этой функции должен иметь отступ в 4 пробела
    title = data.get('name', 'Название неизвестно')
    year = data.get('year', 'Год неизвестен')
    description = data.get('description', 'Описание отсутствует.')

    # Пример отформатированного сообщения
    response_message = f"<b>{title} ({year})</b>\n{description}"

    return response_message
