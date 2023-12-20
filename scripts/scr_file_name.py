import time
import hashlib

def generate_file_name(triangle_colors):
    """
    Генерирует имя файла на основе Unix timestamp и хеша цветов треугольников.

    :param triangle_colors: Список цветов треугольников в формате [(R, G, B), ...].
    :return: Имя файла в формате {timestamp}_{colors_hash}.png.
    """
    # Получаем Unix timestamp
    timestamp = int(time.time())

    # Преобразуем цвета в строку для хеширования
    colors_str = str(triangle_colors)

    # Вычисляем MD5 хеш цветов
    colors_hash = hashlib.md5(colors_str.encode()).hexdigest()

    # Получаем первые 12 символов хеша
    truncated_hash = colors_hash[:12]

    # Формируем имя файла
    file_name = f"{timestamp}_{truncated_hash}.png"

    return file_name

# Пример использования
triangle_colors_example = [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]
result_file_name = generate_file_name(triangle_colors_example)
print(result_file_name)
