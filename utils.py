import sys
import os


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    PyInstaller создает временную папку в _MEIPASS.
    """
    try:
        # PyInstaller создает временную папку в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    # Для отладки
    if not os.path.exists(full_path) and not getattr(sys, 'frozen', False):
        print(f"WARNING: Resource not found: {full_path}")

    return full_path