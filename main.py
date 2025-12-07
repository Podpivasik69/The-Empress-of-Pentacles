import view
import arcade

font = 'minecraft.ttf'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(view.SCREEN_WIDTH, view.SCREEN_HEIGHT, view.SCREEN_TITLE)
    start_view = view.StartMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
