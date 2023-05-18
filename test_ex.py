colour =  (224, 93, 40)
alfa = 128

color_with_alpha = (224, 93, 40) + (alfa,)

invert_colour = colour[::-1]

print(colour)
print('')
print(color_with_alpha)
print('')
print(invert_colour)

def calculate_scale_factor(resolution, base_resolution):
    scale_factor = resolution[0] / base_resolution[0]
    return scale_factor

# Пример использования
resolution = (2560, 1440)  # Разрешение текущего изображения
base_resolution = (1920, 1080)  # Базовое разрешение

scale_factor = calculate_scale_factor(resolution, base_resolution)
print(scale_factor)

scale_var = scale_factor*100
print(scale_var)