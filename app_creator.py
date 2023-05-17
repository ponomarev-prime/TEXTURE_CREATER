from PIL import Image, ImageDraw
import random
import math

def generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, start_color, end_color):
    image = Image.new('RGB', resolution, background_color)
    draw = ImageDraw.Draw(image)
    
    for _ in range(num_triangles):
        triangle_size = random.randint(min_triangle_size, max_triangle_size)
        triangle_color = generate_gradient_color(start_color, end_color)
        
        x1, y1, x2, y2, x3, y3 = generate_triangle_coordinates(resolution, triangle_size)
        vertices = [(x1, y1), (x2, y2), (x3, y3)]
        
        center_x = (x1 + x2 + x3) // 3
        center_y = (y1 + y2 + y3) // 3
        
        # Вращение треугольника
        angle = random.uniform(0, 2*math.pi)
        rotated_vertices = rotate_triangle(vertices, angle, (center_x, center_y))
    
        # Рисование треугольника
        draw.polygon(rotated_vertices, triangle_color)
    
    return image

def generate_gradient_color(start_color, end_color):
    colors = [start_color]
    for _ in range(4):
        mid_color = tuple(int((a + b) / 2) for a, b in zip(colors[-1], end_color))
        colors.append(mid_color)
    colors.append(end_color)
    return random.choice(colors)

def generate_triangle_coordinates(resolution, triangle_size):
    x_range = resolution[0] - triangle_size
    y_range = resolution[1] - triangle_size
    
    x1 = random.randint(0, x_range)
    y1 = random.randint(0, y_range)
    
    x2 = x1 + triangle_size
    y2 = y1
    
    x3 = random.randint(x1, x2)
    y3 = y1 + triangle_size
    
    return x1, y1, x2, y2, x3, y3

def rotate_triangle(vertices, angle, center):
    rotated_vertices = []
    for x, y in vertices:
        x -= center[0]
        y -= center[1]
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        rotated_x += center[0]
        rotated_y += center[1]
        rotated_vertices.append((rotated_x, rotated_y))
    return rotated_vertices

min_triangle_size = 20
max_triangle_size = 100
resolution = (800, 600)
background_color = (255, 255, 255)
start_color = (255, 0, 0)
end_color = (0, 0, 255)
num_triangles = random.randint(50, 100)

texture = generate_texture(min_triangle_size, max_triangle_size, resolution, background_color, start_color, end_color)
texture.save('generated_texture.png')