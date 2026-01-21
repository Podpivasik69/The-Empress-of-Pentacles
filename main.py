from view import StartMenuView, DeathScreenView
from core.game_state import GameState
from view import *
from constants import *
import arcade
import os
import sys

font = 'Minecraft'
MENU_FONT = 'Minecraft'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")



print(f"Python версия: {sys.version}")
print(f"Arcade версия: {arcade.__version__}")
print(f"Arcade путь: {arcade.__file__}")

# Проверяем, есть ли метод configure
print(f"Есть ли arcade.configure? {hasattr(arcade, 'configure')}")

# Смотрим все атрибуты arcade
print("\nДоступные атрибуты arcade (первые 20):")
for attr in dir(arcade)[:20]:
    print(f"  {attr}")

# оставь надежду всяк сюда входящий...
# привет, если ты читаешь это то тебе инетересна моя игра или ее код
# сейчас расскажу как у меня тут все устроено
# main          - точка входа в игру
# view          - код для отрисовки разных штучек типо меню, экрана главной игры и тд
# player        - код в котором пока что вся игровая логика
# staff         - код разных магических посохов
# projectile    - код для балистического расчета полета снарядов по параболе
# ui_components - отрисовка всяких игровых элементов типо инвенторя, квик бара с заклинаниями и другие
# monster       - там логика монстриков
# elemental_circle - элементальный круг, все ясно с ним
# elemental_binding.json - бинды для кнопочек (удобно!)
# зона ужаса ниже
# physics - код физики - писал марк я хз чотам
# world   - отрисовка игрового мира, процедурная генерация


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_state = GameState()

    if game_state.TEST_MODE:
        game_view = GameView()  # переключаем окно на игру
        game_view.setup()  # запускаем игровой setuo
        window.show_view(game_view)  # показываем окно игры
        print(f"запуск в тестовом режиме. Шрифт меню: {MENU_FONT}")
    else:
        start_view = StartMenuView()
        window.show_view(start_view)
        print(f"запуск через меню. Шрифт: {MENU_FONT}")

    arcade.run()


if __name__ == "__main__":
    main()
