import arcade


class CursorManager:
    def __init__(self, game_state):
        self.game_state = game_state
        self.crosshair_list = arcade.SpriteList()  # прицел

        # Созда7гите прицела
        crosshair_sprite = arcade.Sprite('media/staffs/crosshair.png', scale=0.5)
        crosshair_sprite.center_x = self.game_state.cursor_x
        crosshair_sprite.center_y = self.game_state.cursor_y
        self.crosshair_list.append(crosshair_sprite)

    def update_position(self):
        if self.crosshair_list and len(self.crosshair_list) > 0:
            self.crosshair_list[0].center_x = self.game_state.cursor_x
            self.crosshair_list[0].center_y = self.game_state.cursor_y

    def draw(self):
        self.crosshair_list.draw()
