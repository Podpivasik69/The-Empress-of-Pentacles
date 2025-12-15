import arcade
import random

# Константы
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Цветущие лилии"
FLOWER_COUNT = 10
ANIMATION_SPEED = 0.2  # скорость анимации в секундах между кадрами


class Flower(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 1. Загрузите все 9 текстур анимации в список self.textures.
        # 2. Установите начальную текстуру (бутон).
        # 3. Задайте позицию и масштаб спрайта.
        self.default_text = arcade.load_texture('images/flowers/flower0.png')

        self.animation_frame = 0
        self.is_blooming = False
        self.animation_timer = 0

    def update(self, delta_time: float = 1 / 60):
        # Если is_blooming равно True, увеличивайте animation_timer.
        # Когда таймер превысит ANIMATION_SPEED:
        # - Сбросьте таймер, увеличьте кадр анимации (animation_frame).
        # - Смените текущую текстуру спрайта на новую из списка.
        # - Если анимация дошла до конца, установите is_blooming в False.
        ...

    def start_blooming(self):  # Изменение параметра цветения
        # Установите флаг is_blooming в True, чтобы запустить анимацию.
        ...


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Загрузите фоновую текстуру 'images/meadow.png'.
        self.backgroung = arcade.load_texture('images/meadow.png')

    def setup(self):
        self.flower_list = arcade.SpriteList()
        # Создайте FLOWER_COUNT экземпляров класса Flower в случайных
        # позициях и добавьте их в self.flower_list.
        ...

    def on_draw(self):
        self.clear()
        # Отрисуйте фон и список цветов self.flower_list.
        arcade.draw_texture_rect(self.backgroung,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))

    def on_update(self, delta_time):
        # Вызовите метод .update() у всего списка спрайтов, передав delta_time.
        # Это автоматически вызовет метод update() у каждого цветка.
        ...

    def on_mouse_press(self, x, y, button, modifiers):
        # Используйте arcade.get_sprites_at_point, чтобы найти нажатые цветки.
        # Для каждого из них вызовите метод start_blooming().
        ...


def setup_game(width=1000, height=500, title="Цветущие лилии"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
