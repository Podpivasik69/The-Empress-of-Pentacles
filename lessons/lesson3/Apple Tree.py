import arcade
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
TITLE = "Apple Tree"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # Загрузите фоновую текстуру 'images/tree.png'
        self.apple_tree_background = arcade.load_texture('images/tree.png')
        # Инициализируйте два списка спрайтов:
        # self.apple_list — для яблок на дереве
        # self.apple_hit_list — для падающих яблок
        self.apple_list = arcade.SpriteList()
        self.apple_hit_list = arcade.SpriteList()

    def setup(self):
        """Настройка игры"""
        # В цикле создайте 10 спрайтов яблок ('images/apple.png').
        # Для каждого задайте случайные координаты в пределах кроны дерева (150 пикселей от краев экрана)
        # и добавьте его в self.apple_list.
        for _ in range(10):
            apple = arcade.Sprite('images/apple.png', scale=1.0)
            apple.center_x = random.randint(150, 850)
            apple.center_y = random.randint(150, 650)
            self.apple_list.append(apple)

    def on_draw(self):
        self.clear()
        # Сначала нарисуйте фоновую текстуру.
        arcade.draw_texture_rect(self.apple_tree_background,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        # Затем отрисуйте оба списка спрайтов с помощью метода .draw().
        self.apple_list.draw()
        self.apple_hit_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мышью"""
        # Используйте arcade.get_sprites_at_point для определения,
        # по какому яблоку из self.apple_list был сделан клик.
        # Переместите "кликнутые" яблоки из self.apple_list в self.apple_hit_list.
        clicker_aple = arcade.get_sprites_at_point((x, y), self.apple_list)
        for aplle in clicker_aple:
            aplle.remove_from_sprite_lists()
            self.apple_hit_list.append(aplle)

    def on_update(self, delta_time: float):
        """Обновление состояния игры"""
        # В цикле пройдитесь по списку падающих яблок (self.apple_hit_list).
        # Для каждого яблока уменьшите его center_y, используя скорость и delta_time.
        # Проверьте, не достигло ли яблоко низа окна, и остановите его.
        for bad_apple in range(len(self.apple_hit_list)):
            if self.apple_hit_list[bad_apple].center_y - self.apple_hit_list[bad_apple].height / 2 > 0:
                self.apple_hit_list[bad_apple].center_y -= 50 * delta_time


def setup_game(width=1000, height=800, title="Apple Tree"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
