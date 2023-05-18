import cv2
import numpy as np
import random
import math

def generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, background_alfa, triangle_colors, triangle_alfa):
    image = np.zeros((resolution[1], resolution[0], 4), dtype=np.uint8)
    
    image[:, :, 0:3] = background_color[::-1] # Фон
    image[:, :, 3] = background_alfa  # Установка альфа-канала 
    
    for _ in range(num_triangles):
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        
        triangle_color = convert_rgb_to_bgr(random.choice(triangle_colors))
        
        x, y, w, h, angle = generate_triangle_properties(resolution, triangle_size)

        # Создание треугольника
        triangle = np.array([(x, y), (x + w, y), (x, y + h)], np.int32)
        rotated_triangle = rotate_triangle(triangle, angle, (x + w/2, y + h/2))
        
        # Alfa
        triangle_color = triangle_color + (triangle_alfa,)
        print(triangle_color)
        
        # Заполнение треугольника сглаженным цветом. Функция cv2.fillPoly() ожидает цвет в формате (B, G, R) или (B, G, R, A)
        cv2.fillPoly(image, [rotated_triangle], triangle_color, lineType=cv2.LINE_AA)

    return image

# (R, G, B) > (B, G, R)
def convert_rgb_to_bgr(rgb_color):
    bgr_color = (rgb_color[2], rgb_color[1], rgb_color[0])
    return bgr_color

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

# Параметры текстуры
# Размер треугольников
min_triangle_size = 128
max_triangle_size = 256
# Колличество треугольников
num_triangles = random.randint(128, 196)
# Разрешение
resolution = (2560, 1440)
# Фон (R, G, B)
background_color = (2, 1, 1)
background_alfa = 255
# Цвета (R, G, B)
triangle_colors = [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]
triangle_alfa = 255

# Создание текстуры
texture = generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, background_alfa, triangle_colors, triangle_alfa)

# Сохранение текстуры в файл
cv2.imwrite('generated_texture.png', texture)

