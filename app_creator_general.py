import cv2
import numpy as np
import random
import math

def generate_texture(num_triangles, min_triangle_size, max_triangle_size, resolution, background_color, background_alfa, triangle_colors, triangle_alfa):
    image = np.zeros((resolution[1], resolution[0], 4), dtype=np.uint8)
    
    image[:, :, 0:3] = background_color[::-1] # Фон (R, G, B) > (B, G, R)
    image[:, :, 3] = background_alfa  # Установка альфа-канала 
    
    for _ in range(num_triangles):
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        
        triangle_color = random.choice(triangle_colors)[::-1]
        
        x, y, w, h, angle = generate_triangle_properties(resolution, triangle_size)

        # Создание треугольника
        triangle = np.array([(x, y), (x + w, y), (x, y + h)], np.int32)
        rotated_triangle = rotate_triangle(triangle, angle, (x + w/2, y + h/2))
        
        # Alfa
        triangle_color = triangle_color + (triangle_alfa,)
        
        # Заполнение треугольника сглаженным цветом. Функция cv2.fillPoly() ожидает цвет в формате (B, G, R) или (B, G, R, A)
        cv2.fillPoly(image, [rotated_triangle], triangle_color, lineType=cv2.LINE_AA)

    return image

def generate_triangle_properties(resolution, triangle_size):
    x_range = resolution[0] - triangle_size
    y_range = resolution[1] - triangle_size

    x = random.randint(0, x_range)
    y = random.randint(0, y_range)

    w = random.randint(0, triangle_size)
    h = random.randint(0, triangle_size)

    angle = random.uniform(0, 2*math.pi)

    return x, y, w, h, angle

def rotate_triangle(triangle, angle, center):
    rotated_triangle = []
    for x, y in triangle:
        x -= center[0]
        y -= center[1]
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        rotated_x += center[0]
        rotated_y += center[1]
        rotated_triangle.append((rotated_x, rotated_y))
    return np.array(rotated_triangle, np.int32)

def calculate_scale_factor(resolution, base_resolution=(1920, 1080), base_scale_factor=100):
    """
    Рассчитывает масштабирующий коэффициент (scale_factor) на основе разрешения.

    :param resolution: Кортеж, представляющий разрешение в формате (ширина, высота).
    :param base_resolution: Базовое разрешение, для которого установлен базовый масштабный коэффициент.
    :param base_scale_factor: Базовый масштабный коэффициент, соответствующий базовому разрешению.
    :return: Вычисленный масштабирующий коэффициент.
    """
    base_width, base_height = base_resolution
    width, height = resolution

    # Вычисление среднего значения разрешения
    average_resolution = (width + height) / 2

    # Вычисление масштабного коэффициента
    scale_factor = base_scale_factor * (average_resolution / ((base_width + base_height) / 2))

    return scale_factor

def generate_unique_colors(num_colors, background_color, min_distance=50):
    """
    Генерирует уникальные цвета, не повторяющиеся и не слишком близкие к фоновому цвету.

    :param num_colors: Количество цветов для генерации.
    :param background_color: Фоновый цвет в формате (R, G, B).
    :param min_distance: Минимальное расстояние между созданными цветами.
    :return: Список уникальных цветов в формате [(R, G, B), ...].
    """
    colors = []

    def calculate_color_distance(color1, color2):
        return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

    def is_color_too_close(new_color, existing_colors):
        for color in existing_colors:
            if calculate_color_distance(new_color, color) < min_distance:
                return True
        return False

    for _ in range(num_colors):
        while True:
            new_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            if not is_color_too_close(new_color, colors) and calculate_color_distance(new_color, background_color) >= min_distance:
                colors.append(new_color)
                break

    return colors


def create_triangle_texture_image():
    # имя файла
    file_name = 'texture_general.png'

    # Параметры треугольников
    min_triangle_size = 128
    max_triangle_size = 256
    num_triangles = random.randint(128, 196)

    # Параметры текстуры
    resolution = (2560, 1440)
    background_color = (2, 1, 1)

    # Альфа-канал
    background_alfa = 255
    triangle_alfa = 255

    triangle_colors = generate_unique_colors(4, background_color) # [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]

    # Масштабирование треугольников
    scale_factor = calculate_scale_factor(resolution)
    scale_var = scale_factor / 100

    # Создание текстуры
    texture = generate_texture(num_triangles, int(min_triangle_size * scale_var), int(max_triangle_size * scale_var),
                                resolution, background_color, background_alfa, triangle_colors, triangle_alfa)

    # Сохранение текстуры в файл
    cv2.imwrite(file_name, texture)

if __name__ == "__main__":
    create_triangle_texture_image()