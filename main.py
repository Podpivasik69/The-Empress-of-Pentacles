import arcade  # Подключаем игровые суперсилы
from view import *
from player import *

a = 1000
b = 'sex'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"
font = 'minecraft.ttf'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
