import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path) and not getattr(sys, 'frozen', False):
        print(f"not found {full_path}")

    return full_path