import cv2
import numpy as np
import random

def generate_texture(resolution, min_triangle_size, max_triangle_size, background_color, triangle_colors, num_triangles):
    image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
    image[:] = background_color
    
    placed_triangles = 0
    existing_triangles = []
    
    while placed_triangles < num_triangles:
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        triangle_color = random.choice(triangle_colors)[::-1]
        
        x = random.randint(0, resolution[0] - triangle_size)
        y = random.randint(0, resolution[1] - triangle_size)
        
        if not is_triangles_intersecting((x, y, triangle_size), existing_triangles):
            place_triangle(x, y, triangle_size, image, triangle_color)
            existing_triangles.append((x, y, triangle_size))
            placed_triangles += 1
    
    return image

def is_triangles_intersecting(new_triangle, existing_triangles):
    for triangle in existing_triangles:
        if is_intersecting(new_triangle, triangle):
            return True
    return False

def is_intersecting(triangle1, triangle2):
    t1_v1, t1_v2, t1_v3 = triangle1
    t2_v1, t2_v2, t2_v3 = triangle2

def is_point_inside_triangle(point, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    d1 = sign(point, v1, v2)
    d2 = sign(point, v2, v3)
    d3 = sign(point, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

    if (
        is_point_inside_triangle(t1_v1, t2_v1, t2_v2, t2_v3) or
        is_point_inside_triangle(t1_v2, t2_v1, t2_v2, t2_v3) or
        is_point_inside_triangle(t1_v3, t2_v1, t2_v2, t2_v3) or
        is_point_inside_triangle(t2_v1, t1_v1, t1_v2, t1_v3) or
        is_point_inside_triangle(t2_v2, t1_v1, t1_v2, t1_v3) or
        is_point_inside_triangle(t2_v3, t1_v1, t1_v2, t1_v3)
    ):
        return True

    return False

def place_triangle(x, y, size, image, color):
    triangle_points = [
        (x, y),
        (x + size, y),
        (x + size / 2, y + size)
    ]
    
    triangle_points = np.array(triangle_points, dtype=np.int32)
    cv2.fillPoly(image, [triangle_points], color, lineType=cv2.LINE_AA)

def rotate_triangle(image, center, angle):
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_image = cv2.warpAffine(image, M, (cols, rows))
    return rotated_image

# Параметры текстуры
resolution = (1920, 1080)
min_triangle_size = 50
max_triangle_size = 100
background_color = (2, 1, 1)
triangle_colors = [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]
num_triangles = 100

# Создание текстуры
texture = generate_texture(resolution, min_triangle_size, max_triangle_size, background_color, triangle_colors, num_triangles)

# Сохранение текстуры в файл
cv2.imwrite('texture_monte-carlo_method.png', texture)
