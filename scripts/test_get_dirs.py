import os

def get_directory(directory_type='current'):
    """
    Получает текущую или родительскую директорию в зависимости от параметра.

    :param directory_type: Тип директории: 'current' для текущей директории, 'parent' для родительской.
    :return: Путь к выбранной директории.
    """
    current_directory = os.path.abspath(os.path.dirname(__file__))  # Директория, в которой расположен скрипт

    if directory_type == 'current':
        return current_directory
    elif directory_type == 'parent':
        return os.path.abspath(os.path.join(current_directory, os.pardir))
    else:
        raise ValueError("Invalid directory_type. Use 'current' or 'parent'.")

# Пример использования
current_dir = get_directory('current')
parent_dir = get_directory('parent')

print(f"Current Directory: {current_dir}")
print(f"Parent Directory: {parent_dir}")
