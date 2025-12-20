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
        self.texture_list = list()
        for _ in range(9):
            t = arcade.load_texture(f'images/flowers/flower{_}.png')
            self.texture_list.append(t)
        self.texture = self.texture_list[0]
        self.animation_frame = 0
        self.is_blooming = False
        self.animation_timer = 0
        self.center_y = y
        self.center_x = x
        self.scale = 0.3

    def update(self, delta_time: float = 1 / 60):
        # Если is_blooming равно True, увеличивайте animation_timer.
        # Когда таймер превысит ANIMATION_SPEED:
        # - Сбросьте таймер, увеличьте кадр анимации (animation_frame).
        # - Смените текущую текстуру спрайта на новую из списка.
        # - Если анимация дошла до конца, установите is_blooming в False.
        if self.is_blooming:
            self.animation_timer += 1 * delta_time
        if self.animation_timer > ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_frame += 1

            if self.animation_frame < 9:
                self.texture = self.texture_list[self.animation_frame]
            else:
                self.is_blooming = False

    def start_blooming(self):  # Изменение параметра цветения
        # Установите флаг is_blooming в True, чтобы запустить анимацию.
        self.is_blooming = True
        self.animation_frame = 0
        self.texture = self.texture_list[0]


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Загрузите фоновую текстуру 'images/meadow.png'.
        self.backgroung = arcade.load_texture('images/meadow.png')

    def setup(self):
        self.flower_list = arcade.SpriteList()
        # Создайте FLOWER_COUNT экземпляров класса Flower в случайных
        # позициях и добавьте их в self.flower_list.
        for _ in range(FLOWER_COUNT):
            self.flower_list.append(
                Flower(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)))

    def on_draw(self):
        self.clear()
        # Отрисуйте фон и список цветов self.flower_list.
        arcade.draw_texture_rect(self.backgroung,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.flower_list.draw()

    def on_update(self, delta_time):
        # Вызовите метод .update() у всего списка спрайтов, передав delta_time.
        # Это автоматически вызовет метод update() у каждого цветка.
        self.flower_list.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        # Используйте arcade.get_sprites_at_point, чтобы найти нажатые цветки.
        # Для каждого из них вызовите метод start_blooming().
        clicked_flower = arcade.get_sprites_at_point((x, y), self.flower_list)
        for flow in clicked_flower:
            flow.start_blooming()


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
