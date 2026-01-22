# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

block_cipher = None

# Получаем путь к проекту
project_path = os.path.dirname(os.path.abspath(__file__))

# Собираем все медиа файлы
def collect_media_files():
    media_files = []
    media_path = os.path.join(project_path, 'media')

    for root, dirs, files in os.walk(media_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.ico', '.ttf', '.aseprite', '.json')):
                src = os.path.join(root, file)
                # Вычисляем относительный путь для dest
                rel_path = os.path.relpath(root, media_path)
                if rel_path == '.':
                    dest = 'media'
                else:
                    dest = os.path.join('media', rel_path)
                media_files.append((src, dest))

    return media_files

# Собираем все данные
datas = [
    ('media/MinecraftDefault-Regular.ttf', '.'),
     ('media', 'media'),
    ('elemental_bindings.json', '.'),
    ('settings.json', '.'),
    ('constants.py', '.'),
    ('utils.py', '.'),
    ('elemental_circle.py', '.'),
    ('game.py', '.'),
    ('levels.py', '.'),
    ('physics.py', '.'),
    ('player.py', '.'),
    ('world.py', '.'),
    ('spell_system.py', '.'),
    ('staff.py', '.'),
    ('ui_components.py', '.'),
    ('view.py', '.'),
]

# Добавляем медиа файлы
datas.extend(collect_media_files())

# Добавляем папку core
core_path = os.path.join(project_path, 'core')
if os.path.exists(core_path):
    for root, dirs, files in os.walk(core_path):
        for file in files:
            if file.endswith('.py'):
                src = os.path.join(root, file)
                rel_path = os.path.relpath(root, project_path)
                datas.append((src, rel_path))

# Добавляем папку integra
integra_path = os.path.join(project_path, 'integra')
if os.path.exists(integra_path):
    for root, dirs, files in os.walk(integra_path):
        for file in files:
            if file.endswith('.py'):
                src = os.path.join(root, file)
                rel_path = os.path.relpath(root, project_path)
                datas.append((src, rel_path))

a = Analysis(
    ['main.py'],  # Точка входа
    pathex=[project_path],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'arcade',
        'pyglet',
        'json',
        'math',
        'random',
        'os',
        'sys',
        'typing',
        'collections',
        'pathlib',
        'time',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'tkinter',
        'PyQt5',
        'PySide2',
        'test',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='The_Empress_of_Pentacles',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Изменил на False чтобы не показывать консоль
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='media/icon.ico',
)

# Если нужен one-folder вместо one-file, добавь:
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.datas,
#     a.zipfiles,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='The_Empress_of_Pentacles'
# )