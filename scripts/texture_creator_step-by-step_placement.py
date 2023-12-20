import cv2
import numpy as np
import random
import math

def generate_texture(resolution, min_triangle_size, max_triangle_size, background_color, triangle_colors, num_triangles):

    image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
    image[:] = background_color
    
    triangles = []  # Список для хранения треугольников и их позиций
    placed_triangles = 0  # Счетчик размещенных треугольников
    
    for _ in range(num_triangles):
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        triangle_color = random.choice(triangle_colors)[::-1]
        
        while True:
            x = random.randint(0, resolution[0] - triangle_size)
            y = random.randint(0, resolution[1] - triangle_size)
            
            # Проверяем, не пересекается ли треугольник с другими треугольниками
            is_intersecting = False
            for existing_triangle in triangles:
                if is_triangles_intersecting((x, y), triangle_size, existing_triangle):
                    is_intersecting = True
                    break
            
            if not is_intersecting:
                break
        
        triangle = generate_rotated_triangle(x, y, triangle_size, random.uniform(0, 2 * math.pi))
        cv2.fillPoly(image, [triangle], triangle_color, lineType=cv2.LINE_AA)
        
        triangles.append((x, y, triangle_size))
        
        placed_triangles += 1
        print(placed_triangles)
    
    return image

def is_triangles_intersecting(pos, size, existing_triangle):
    x1, y1 = pos
    x2, y2, size2 = existing_triangle
    
    x1_center = x1 + size // 2
    y1_center = y1 + size // 2
    x2_center = x2 + size2 // 2
    y2_center = y2 + size2 // 2
    
    distance = math.sqrt((x1_center - x2_center)**2 + (y1_center - y2_center)**2)
    max_distance = (size + size2) / 2
    
    return distance < max_distance

def generate_rotated_triangle(x, y, size, angle):
    half_size = size // 2
    vertices = np.array([
        (x - half_size, y + half_size),
        (x + half_size, y + half_size),
        (x, y - half_size)
    ], np.float32)
    
    center = (x, y)
    
    rotation_matrix = cv2.getRotationMatrix2D(center, math.degrees(angle), 1.0)
    rotated_vertices = cv2.transform(np.array([vertices]), rotation_matrix)[0]
    
    return np.round(rotated_vertices).astype(np.int32)

# Пример использования
resolution = (1920, 1080)  # Разрешение изображения
min_triangle_size = 50
max_triangle_size = 150
background_color = (2, 1, 1)
triangle_colors = [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]
num_triangles = 90  # Желаемое количество треугольников

texture = generate_texture(resolution, min_triangle_size, max_triangle_size, background_color, triangle_colors, num_triangles)

cv2.imwrite('texture_step-by-step_placement.png', texture)
