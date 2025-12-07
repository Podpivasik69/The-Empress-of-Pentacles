from main import *
import arcade


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