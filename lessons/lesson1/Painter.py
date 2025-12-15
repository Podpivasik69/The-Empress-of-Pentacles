import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Drop balls"
VELOCITY = 2


class MyGame(arcade.Window):
    def __init__(self, width, height, title, velocity):
        super().__init__(width, height, title)
        self.velocity = velocity
        self.mouse_pressed = False
        self.mouse_x = 0
        self.mouse_y = 0

    def setup(self):
        self.points = []
        self.speed = []
        self.radius = 20

    def on_draw(self):
        self.clear()

        for i in range(len(self.points)):
            x, y = self.points[i]
            dx, dy = self.speed[i]

            x += dx
            y += dy

            if x - self.radius < 0:
                x = self.radius
                dx = -dx
            elif x + self.radius > self.width:
                x = self.width - self.radius
                dx = -dx

            if y - self.radius < 0:
                y = self.radius
                dy = -dy
            elif y + self.radius > self.height:
                y = self.height - self.radius
                dy = -dy

            self.points[i] = [x, y]
            self.speed[i] = [dx, dy]

            arcade.draw_circle_filled(x, y, self.radius, arcade.color.WHITE)

        # Если кнопка зажата, создаем новый шарик
        if self.mouse_pressed:
            self.points.append([self.mouse_x, self.mouse_y])
            velocity_value = self.velocity / (2 ** 0.5)
            self.speed.append([-velocity_value, velocity_value])

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = True
            self.mouse_x = x
            self.mouse_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pressed:
            self.mouse_x = x
            self.mouse_y = y


def setup_game(width=800, height=600, title="Drop balls", velocity=2):
    game = MyGame(width, height, title, velocity)
    game.setup()
    return game


def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
