# core/ui_renderer.py - отрисовка ui пользователя
from ui_components import HealthBar
import core.game_state
import arcade

QUICKBAR_POS = (150, 550)
QUICKBAR_SIZE = (256, 64)
SLOT_POSITIONS = [(54, 550), (118, 550), (182, 550), (246, 550)]


class UIRenderer:
    def __init__(self, game_state):
        self.game_state = game_state
        self.health_bar = None  # пока не создан, создается в setup

        self.crosshair_list = arcade.SpriteList()  # прицел
        self.spell_progressbar_sprite = arcade.Sprite('media/ui/spell_progressbar.png', scale=1.0)
        self.spell_icons = {}  # кэш для картинок спелов
        # прогресс бар
        self.progressbar_spritelist = arcade.SpriteList()
        self.progressbar_spritelist.append(self.spell_progressbar_sprite)

        # квик бар
        self.quickbar_texture = None
        self.slot_highlight_texture = None

    def setup(self):
        """ Создает Ui обьекты"""
        self.health_bar = HealthBar(
            max_health=self.game_state.player.max_health,
            position=(400, 530),
            size=(200, 20),
            scale=1.0,
            frame_texture_path="media/ui/hp_progressbar.png"
        )
        self.quickbar_texture = arcade.load_texture('media/ui/quickbar.png')
        self.slot_highlight_texture = arcade.load_texture("media/slot_highlight.png")

    def update(self):
        """ Логика обновления Ui"""

    def draw(self):
        """ Отрисовка Ui"""

    def draw_quickbar(self):
        # отрисовка квик бара
        arcade.draw_texture_rect(self.quickbar_texture, arcade.rect.XYWH(150, 550, 256, 64), )

        # квик бар
        for i, spell in enumerate(self.game_state.ready_spells):
            if i < 4:
                if spell in self.game_state.spell_icons:
                    texture = self.game_state.spell_icons[spell]
                    arcade.draw_texture_rect(
                        texture,
                        arcade.rect.XYWH(SLOT_POSITIONS[i][0], SLOT_POSITIONS[i][1], 48, 48)
                    )
        # подсветка иконок
        if 0 <= self.game_state.selected_spell_index < 4:
            highlight_x = SLOT_POSITIONS[self.game_state.selected_spell_index][0]
            highlight_y = SLOT_POSITIONS[self.game_state.selected_spell_index][1]
            arcade.draw_texture_rect(
                self.slot_highlight_texture,
                arcade.rect.XYWH(highlight_x, highlight_y, 64, 64)
            )
