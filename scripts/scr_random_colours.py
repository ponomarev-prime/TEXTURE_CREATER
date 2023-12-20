import random

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

# Пример использования
background_color = (2, 1, 1)
generated_colors = generate_unique_colors(4, background_color)

print("Сгенерированные уникальные цвета:")
#for color in generated_colors:
#    print(color)
# print("---")

print(generated_colors)