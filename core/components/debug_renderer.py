# core/debug_renderer.py
import arcade.color


class DebugPanel:
    """ Универсальный компонет для вывода всякой хуйни"""

    def __init__(self, category, x, y, follow_object, get_world_coords_func, get_screen_coords_func=None):
        self.enabled = False
        self.category = category
        self.color = arcade.color.WHITE
        self.x = x
        self.y = y
        self.lines = []  # список строк данных

        self.follow_object = follow_object
        self.offset_y = 40  # смещение по y

        self.get_world_coords = get_world_coords_func
        self.get_screen_coords = get_screen_coords_func

    def toggle(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True

    def add_line(self, text):
        self.lines.append((text, self.color))

    def update_position(self, screen_x, screen_y):
        self.x = screen_x
        self.y = screen_y + self.offset_y

    def draw(self):
        if not self.enabled:
            return
        current_y = self.y
        for text, color in self.lines:
            arcade.draw_text(text, self.x, current_y, color, 14, anchor_x="center", anchor_y="bottom")
            current_y -= 20


class DebugRenderer:
    def __init__(self, game_state):
        self.game_state = game_state
        self.enabled = True

        self.player_panel = self._create_player_panel()

        self.enemy_panels = []

    def _create_player_panel(self):
        if not self.game_state.player:
            return None

        def get_player_world_coords():
            return (self.game_state.player.world_x,
                    self.game_state.player.world_y)

        def get_player_screen_coords():
            if self.game_state.camera_manager:
                return self.game_state.camera_manager.world_to_screen(
                    self.game_state.player.world_x,
                    self.game_state.player.world_y
                )
            return (self.game_state.player.world_x,
                    self.game_state.player.world_y)

        panel = DebugPanel(
            category="player",
            get_world_coords_func=get_player_world_coords,
            get_screen_coords_func=get_player_screen_coords
        )
        return panel

    def _create_enemy_panel(self, enemy):
        def get_enemy_world_coords():
            return (enemy.x, enemy.y)

        def get_enemy_screen_coords():
            if self.game_state.camera_manager:
                return self.game_state.camera_manager.world_to_screen(
                    enemy.x, enemy.y
                )
            return (enemy.x, enemy.y)

        panel = DebugPanel(
            category=f"enemy_{id(enemy)}",
            get_world_coords_func=get_enemy_world_coords,
            get_screen_coords_func=get_enemy_screen_coords
        )
        return panel

    def update(self, delta_time):
        if not self.enabled:
            return

        if self.player_panel:
            self._update_panel(self.player_panel)

        self._update_enemy_panels()

    def _update_panel(self, panel):

        panel.lines.clear()
        world_x, world_y = panel.get_world_coords()
        screen_x, screen_y = panel.get_screen_coords()

        panel.update_position(screen_x, screen_y)
        panel.add_line(f"World: ({world_x:.1f}, {world_y:.1f})")
        panel.add_line(f"Screen: ({screen_x:.1f}, {screen_y:.1f})")

        if abs(screen_x - world_x) < 1 and abs(screen_y - world_y) < 1:
            panel.color = arcade.color.RED
        else:
            panel.color = arcade.color.WHITE

    def _update_enemy_panels(self):
        self.enemy_panels.clear()

        for enemy in self.game_state.enemies:
            if enemy.is_alive:
                panel = self._create_enemy_panel(enemy)
                self._update_panel(panel)
                self.enemy_panels.append(panel)

    # TODO ЭКСТЕРМИНАТУС ЕРЕСИ
    def draw(self, camera_manager):
        if not self.enabled:
            return

        if not camera_manager or not self.game_state.player:
            return

        player_world_x = self.game_state.player.world_x
        player_world_y = self.game_state.player.world_y
        player_screen_x, player_screen_y = camera_manager.world_to_screen(player_world_x, player_world_y)

        arcade.draw_text(
            f"P W: {player_world_x:.1f}, {player_world_y:.1f}",
            player_screen_x, player_screen_y + 50,
            arcade.color.WHITE, 14, anchor_x="center"
        )
        arcade.draw_text(
            f"P S: {player_screen_x:.1f}, {player_screen_y:.1f}",
            player_screen_x, player_screen_y + 30,
            arcade.color.GREEN, 14, anchor_x="center"
        )

        for enemy in self.game_state.enemies:
            if enemy.is_alive:
                enemy_world_x, enemy_world_y = enemy.x, enemy.y
                enemy_screen_x, enemy_screen_y = camera_manager.world_to_screen(enemy_world_x, enemy_world_y)

                if abs(enemy_screen_x - enemy_world_x) < 1 and abs(enemy_screen_y - enemy_world_y) < 1:
                    text_color = arcade.color.RED
                else:
                    text_color = arcade.color.YELLOW

                arcade.draw_text(
                    f"E W: {enemy_world_x:.1f}, {enemy_world_y:.1f}",
                    enemy_screen_x, enemy_screen_y + 50,
                    text_color, 14, anchor_x="center"
                )
                arcade.draw_text(
                    f"E S: {enemy_screen_x:.1f}, {enemy_screen_y:.1f}",
                    enemy_screen_x, enemy_screen_y + 30,
                    text_color, 14, anchor_x="center"
                )
