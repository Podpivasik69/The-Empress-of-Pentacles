import arcade


class PauseMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

