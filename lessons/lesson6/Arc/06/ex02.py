import arcade

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Тайловый Уровень — Вау!"
TILE_SCALING = 0.5  # Если тайлы 64x64, а хотим чтобы на экране были 64x64 — ставим 1.0


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Здесь будут жить наши списки спрайтов из карты
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте."""
        # Инициализируем списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()  # Сюда попадёт слой Collision!

        # ===== ВОЛШЕБСТВО ЗАГРУЗКИ КАРТЫ! (почти без магии). =====
        # Грузим тайловую карту
        map_name = "first_level.tmx"
        # Параметр 'scaling' ОЧЕНЬ важен! Умножает размер каждого тайла
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # --- Достаём слои из карты как спрайт-листы ---
        # Слой "walls" (стены) — просто для отрисовки
        self.wall_list = tile_map.sprite_lists["walls"]
        # Слой "chests" (сундуки) — красота!
        self.chests_list = tile_map.sprite_lists["chests"]
        # Слой "exit" (выходы с уровня) — красота!
        self.exit_list = tile_map.sprite_lists["exit"]
        # САМЫЙ ГЛАВНЫЙ СЛОЙ: "Collision" — наши стены и платформы для физики!
        self.collision_list = tile_map.sprite_lists["collision"]
        # --- Создаём игрока. ---
        # Карту загрузили, теперь создаём героя, который будет по ней бегать
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           0.5)
        # Ставим игрока куда-нибудь на землю (посмотрите в Tiled, где у вас земля!)
        self.player_sprite.center_x = 128  # Примерные координаты
        self.player_sprite.center_y = 256  # Примерные координаты
        self.player_list.append(self.player_sprite)

        # --- Физический движок ---
        # Используем PhysicsEngineSimple, который знаем и любим
        # Он даст нам движение и коллизии со стенами (self.wall_list)!
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list
        )

    def on_draw(self):
        """Отрисовка экрана."""
        self.clear()

        # Рисуем слои карты в правильном порядке (фон -> земля -> платформы -> декорации -> игрок)
        self.wall_list.draw()
        self.chests_list.draw()
        self.exit_list.draw()
        self.player_list.draw()

        # self.collision_list.draw()  # Обычно НЕ рисуем слой коллизий в финальной игре, но для отладки бывает полезно

    def on_update(self, delta_time):
        """Обновление логики игры."""
        # Обновляем физический движок (двигает игрока и проверяет стены)
        self.physics_engine.update()

        # Двигаем камеру за игроком (центрируем)
        # self.camera.move_to((self.player_sprite.center_x, self.player_sprite.center_y))

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш."""
        # Стандартное управление для PhysicsEngineSimple (как в уроке 2)
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш."""
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.player_sprite.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0


def main():
    """Главная функция."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
