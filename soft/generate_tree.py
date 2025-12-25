import os
import sys


def generate_tree(directory, prefix="", ignore_dirs=None, ignore_files=None):
    """Генерирует древовидную структуру директории"""
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', '.idea', '.vscode', 'lessons', '.venv'}
    if ignore_files is None:
        ignore_files = {'.pyc', '.pyo', '.pyd', '.pyc'}

    try:
        items = os.listdir(directory)
    except PermissionError:
        print(prefix + "└── [Доступ запрещен]")
        return

    items = [item for item in items if not item.startswith('.')]

    # Сначала директории, потом файлы
    dirs = sorted([item for item in items if os.path.isdir(os.path.join(directory, item))])
    files = sorted([item for item in items if not os.path.isdir(os.path.join(directory, item))])

    filtered_dirs = [d for d in dirs if d not in ignore_dirs]
    filtered_files = [f for f in files if not any(f.endswith(ext) for ext in ignore_files)]

    all_items = filtered_dirs + filtered_files

    for i, item in enumerate(all_items):
        is_last = i == len(all_items) - 1
        connector = "└── " if is_last else "├── "

        print(prefix + connector + item)

        path = os.path.join(directory, item)
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            generate_tree(path, prefix + extension, ignore_dirs, ignore_files)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Получаем путь из аргумента
        target_dir = sys.argv[1]
        # Преобразуем в абсолютный путь
        if not os.path.isabs(target_dir):
            target_dir = os.path.abspath(target_dir)
    else:
        # Если аргументов нет, используем родительскую директорию скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.dirname(script_dir)  # Поднимаемся на уровень выше

    print(f"Дерево для: {target_dir}")
    print("=" * 50)
    print(os.path.basename(target_dir) + "/")
    generate_tree(target_dir)
    print("=" * 50)
    print(f"Анализ завершен. Показаны все папки и файлы проекта.")
