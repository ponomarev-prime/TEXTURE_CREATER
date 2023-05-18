import cv2
import numpy as np
import random
import math

def generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, start_color, end_color):
    image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
    image[:] = background_color
    
    for _ in range(num_triangles):
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        triangle_color = generate_gradient_color(start_color, end_color)
        
        x, y, w, h, angle = generate_triangle_properties(resolution, triangle_size)
        
        # Создание треугольника
        triangle = np.array([(x, y), (x + w, y), (x, y + h)], np.int32)
        rotated_triangle = rotate_triangle(triangle, angle, (x + w/2, y + h/2))
        
        # Заполнение треугольника сглаженным цветом
        cv2.fillPoly(image, [rotated_triangle], triangle_color, lineType=cv2.LINE_AA)
    
    return image

def generate_gradient_color(start_color, end_color):
    colors = [start_color]
    for _ in range(4):
        mid_color = tuple(int((a + b) / 2) for a, b in zip(colors[-1], end_color))
        colors.append(mid_color)
    colors.append(end_color)
    return random.choice(colors)

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
min_triangle_size = 120
max_triangle_size = 180
resolution = (1920, 1080)
background_color = (255, 255, 255)
start_color = (255, 0, 0)
end_color = (0, 0, 255)
num_triangles = random.randint(80, 150)

# Создание текстуры
texture = generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, start_color, end_color)

# Сохранение текстуры в файл
cv2.imwrite('generated_texture.png', texture)