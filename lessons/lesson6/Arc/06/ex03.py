import arcade
import random

from pyglet.graphics import Batch

# ---------- Окно и мир ----------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "TMX + стены + бомбы + камера-шейк"
TILE_SCALING = 0.5

BOMBS_COUNT = 16

# ---------- Камера ----------
CAMERA_LERP = 0.12
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)


class TMXCameraBombsDemo(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, antialiasing=True)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()  # Камера для игрового мира
        self.gui_camera = arcade.camera.Camera2D()  # Камера для объектов интерфейса

        # Причина тряски — специальный объект ScreenShake2D
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,  # Трястись будет только то, что попадает в объектив мировой камеры
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )
        # Звук взрыва на будущее
        self.explosion_sound = arcade.load_sound("sounds/explosion1.mp3")

        # Данные уровня
        self.tile_map = None

        # Слои с нашими спрайтами
        self.player_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()

        # Игрок
        self.player = None

        # Границы мира (по карте)
        self.world_width = SCREEN_WIDTH
        self.world_height = SCREEN_HEIGHT

        # Батч для текста
        self.batch = Batch()
        self.text_info = arcade.Text(
            "WASD/стрелки — движение • Столкнись с красно‑серой «бомбой» (астероид) — камера дрожит",
            20, 20, arcade.color.BLACK, 14, batch=self.batch
        )

    def setup(self):
        # Загружаем уровень из TMX-файла
        self.tile_map = arcade.load_tilemap("sec2.tmx", scaling=TILE_SCALING)
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.collision_list = self.tile_map.sprite_lists["collisions"]

        # Уточняем размеры мира по карте
        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * TILE_SCALING)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * TILE_SCALING)

        # Делаем игрока
        self.player_list = arcade.SpriteList()
        self.player = arcade.Sprite("images/girl.png",
                                    scale=0.8)
        self._place_sprite_safely(self.player)  # Ставим туда, где не пересекается со стенами
        self.player_list.append(self.player)

        # Разбрасываем бомбочки
        self.bomb_list = arcade.SpriteList()
        bomb_texture = "images/berry.png"
        for _ in range(BOMBS_COUNT):
            scale = random.uniform(0.1, 0.5)  # Случайный масштаб для каждой бомбы
            bomb = arcade.Sprite(bomb_texture, scale=scale)
            self._place_sprite_safely(bomb)
            self.bomb_list.append(bomb)

        # Физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def _place_sprite_safely(self, sprite: arcade.Sprite, max_tries: int = 200):
        """Ставит спрайт в случайную свободную точку уровня (не пересекается со стенами)."""
        # Размеры софта: чуть меньше, чтобы было проще найти позицию
        half_w = sprite.width / 2
        half_h = sprite.height / 2
        for _ in range(max_tries):
            sprite.center_x = random.uniform(half_w + 4, self.world_width - half_w - 4)
            sprite.center_y = random.uniform(half_h + 4, self.world_height - half_h - 4)
            if not arcade.check_for_collision_with_list(sprite, self.collision_list):
                return
        # Если совсем не нашли — ставим центр карты (аварийно)
        sprite.center_x = self.world_width / 2
        sprite.center_y = self.world_height / 2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_update(self, dt: float):
        self.physics_engine.update()
        self.camera_shake.update(dt)  # Обновляем тряску камеры

        bombs_hit = arcade.check_for_collision_with_list(self.player, self.bomb_list)
        if bombs_hit:  # наткнулись на бомбы
            for b in bombs_hit:
                b.remove_from_sprite_lists()
            self.explosion_sound.play()  # Бадабум!
            self.camera_shake.start()  # Начинаем тряску камеры, она сама остановится через время, указанное в настройках

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP  # Плавность следования камеры
        )

        self.text_bombs = arcade.Text(
            f"Бомб осталось: {len(self.bomb_list)}",
            20, 46, arcade.color.DARK_SLATE_GRAY, 14, batch=self.batch
        )

    def on_draw(self):
        self.clear()

        # 1) Мир
        self.camera_shake.update_camera()
        self.world_camera.use()
        self.wall_list.draw()
        self.player_list.draw()
        self.bomb_list.draw()
        self.camera_shake.readjust_camera()

        # 2) GUI
        self.gui_camera.use()

        self.batch.draw()


def main():
    app = TMXCameraBombsDemo()
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()
