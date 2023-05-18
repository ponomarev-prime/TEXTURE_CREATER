import cv2
import numpy as np
import random
import math

def generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, grid_size):
    image = np.zeros((resolution[1], resolution[0], 3), dtype=np.uint8)
    image[:] = background_color
    
    cell_width = resolution[0] // grid_size[0]
    cell_height = resolution[1] // grid_size[1]
    
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x = i * cell_width
            y = j * cell_height
            cell_triangles = random.randint(1, 4)  # Количество треугольников в ячейке
            
            for _ in range(cell_triangles):
                triangle_size = random.randint(min_triangle_size, max_triangle_size)
                
                triangle_colors = [(224, 93, 40), (122, 85, 58), (68, 49, 42), (92, 65, 57)]
                triangle_color = random.choice(triangle_colors)[::-1]
                                
                x_offset = random.randint(0, cell_width - triangle_size)
                y_offset = random.randint(0, cell_height - triangle_size)
                
                x_pos = x + x_offset
                y_pos = y + y_offset
                
                angle = random.uniform(0, 2 * math.pi)
                triangle = generate_rotated_triangle(x_pos, y_pos, triangle_size, angle)
                
                cv2.fillPoly(image, [triangle], triangle_color, lineType=cv2.LINE_AA)
    
    return image

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
min_triangle_size = 50
max_triangle_size = 150
resolution = (1920, 1080)
background_color = (2, 1, 1)
grid_size = (6, 6)  # Размер сетки (количество ячеек по горизонтали и вертикали)

texture = generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, grid_size)

cv2.imwrite('texture_uniformity_mesh.png', texture)
cv2.waitKey(0)
cv2.destroyAllWindows()