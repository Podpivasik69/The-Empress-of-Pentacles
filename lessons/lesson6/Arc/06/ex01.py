import arcade
import random

from pyglet.graphics import Batch


class GridGame(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, "Пример клеточного поля со спрайтами")
        self.cell_size = 60
        self.all_sprites = arcade.SpriteList()
        # Загружаем текстуры из встроенных ресурсов
        self.grass_texture = arcade.load_texture(":resources:images/tiles/grassCenter.png")
        self.water_texture = arcade.load_texture(":resources:images/tiles/water.png")
        self.coin_texture = arcade.load_texture(":resources:images/items/coinGold.png")
        # Создаём батч для текста
        self.batch = Batch()
        self.text = arcade.Text("Я здесь!",
                                self.cell_size // 2,
                                self.cell_size // 2 - 30,
                                arcade.color.RED, 12,
                                anchor_x="center", batch=self.batch)

    def setup(self):
        self.grid = [[random.choice([0, 1]) for _ in range(10)] for _ in range(10)]  # Сначала генерим чиселки
        for row in range(10):  # Потом создаём спрайтики и заменяем чиселки на спрайтики
            for col in range(10):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2

                # Рисуем основу клетки
                if self.grid[row][col] == 0:
                    grass_sprite = arcade.Sprite(self.grass_texture, scale=0.5)
                    grass_sprite.position = (x, y)
                    self.grid[row][col] = [grass_sprite]
                    self.all_sprites.append(grass_sprite)
                else:
                    water_sprite = arcade.Sprite(self.water_texture, scale=0.5)
                    self.grid[row][col] = [water_sprite]
                    water_sprite.position = (x, y)
                    self.all_sprites.append(water_sprite)
                # 10% шанс появления монетки (потому что всем нужны бесплатные деньги!)
                if random.random() < 0.1:
                    coin_sprite = arcade.Sprite(self.coin_texture, scale=0.5)
                    coin_sprite.position = (x, y - 4)
                    self.all_sprites.append(coin_sprite)
                    self.grid[row][col].append(coin_sprite)

    def on_draw(self):
        self.clear()
        self.all_sprites.draw()

        # Рисуем игрока (потому что без героя — это просто таблица Excel)
        arcade.draw_circle_filled(
            self.cell_size // 2,
            self.cell_size // 2,
            20,
            arcade.color.RED
        )

        self.batch.draw()


def main():
    game = GridGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
