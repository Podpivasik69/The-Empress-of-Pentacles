import arcade  # Подключаем игровые суперсилы

a = 1000
b = 'sex'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"
font = 'minecraft.ttf'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.white = arcade.color.WHITE
        self.brown = arcade.color.COCOA_BROWN
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.menu_button = arcade.load_texture('media/menu_button.png')

    def on_show(self):
        # Вызывается при показе View
        pass

    def on_draw(self):
        # Назван е
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, (SCREEN_HEIGHT * 3) // 4,
                                                  600, 100), self.white, 1)
        arcade.draw_text(SCREEN_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4,
                         self.white, 42, anchor_x="center", anchor_y="center")
        # Кнопка играть
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), )
        arcade.draw_text('иглать', SCREEN_WIDTH // 2, 250, self.white, 42, anchor_x="center", anchor_y="center")
        # кглпка выохода
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), )
        arcade.draw_text('вихад', SCREEN_WIDTH // 2, 150, self.white, 42, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # жмяк и выход
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 100 <= y <= 200:
            arcade.close_window()
        # иглать
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 200 <= y <= 300:
            game_view = GameView()  # переключаем окно на игру
            game_view.setup()  # запускаем игровой setuo
            self.window.show_view(game_view)  # показываем окно игры


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_sprite_list = None
        # текстуры
        self.player_anim_static_textures = []
        self.current_texture = 0
        self.animation_taimer = 0
        # ходить
        self.is_moving = False
        self.witch_speed = 300
        self.keys_pressed = set()
        # таймеры для анимаций
        self.idle_timer = 0.0
        self.animation_frame_timer = 0.0
        self.current_animation_frame = 0
        self.is_idle_animating = False

    def setup(self):
        for i in range(1, 5):
            texture = arcade.load_texture(f'media/witch/Wizard_static_anim{i}.png')
            self.player_anim_static_textures.append(texture)

        self.player_sprite_list = arcade.SpriteList()

        self.player = arcade.Sprite('media/witch/Wizard_static.png')
        self.static_texture = arcade.load_texture('media/witch/Wizard_static.png')
        self.player.texture = self.static_texture
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_sprite_list.append(self.player)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_update(self, delta_time):

        if self.is_moving:
            self.player.texture = self.static_texture
        # Движение героя
        dx, dy = 0, 0
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            dx -= self.witch_speed * delta_time
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            dx += self.witch_speed * delta_time
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            dy += self.witch_speed * delta_time
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            dy -= self.witch_speed * delta_time

        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.player.center_x += dx
        self.player.center_y += dy

        self.player.center_x = max(20, min(SCREEN_WIDTH - 20, self.player.center_x))
        self.player.center_y = max(20, min(SCREEN_HEIGHT - 20, self.player.center_y))

        # если мы идем то таймер 0, флаги
        if dx != 0 or dy != 0:
            self.idle_timer = 0
            self.is_moving = True
            self.is_idle_animating = False
        # если стоим то таймер растер
        else:
            self.idle_timer += delta_time
            self.is_moving = False
        # если мы стоим И СТОИМ ДОЛЬШЕ 1 СЕКУНДЫ
        if self.idle_timer >= 1.0 and self.is_moving == False:
            self.is_idle_animating = True
            self.animation_frame_timer += delta_time

        if self.is_idle_animating:
            if self.animation_frame_timer >= 0.2:
                self.current_animation_frame = (self.current_animation_frame + 1) % 4
                self.animation_frame_timer = 0
                # меняем текстурку
                self.player.texture = self.player_anim_static_textures[self.current_animation_frame]

    def on_draw(self):
        self.clear()
        # arcade.draw_text("тут типа игра", 400, 300, arcade.color.WHITE, 50, anchor_x="center", anchor_y="center")
        self.player_sprite_list.draw()


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
