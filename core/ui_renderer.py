# core/ui_renderer.py - отрисовка ui пользователя
from core.components.ultimate_bar import UltimateBar
from constants import *
import core.game_state
from ui_components import SpellProgressBar
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
        self.spell_progress_bars = []
        self.staff_cooldown_bar = None

        # квик бар
        self.quickbar_texture = None
        self.slot_highlight_texture = None

        # tab
        self.tab_background_sprite = None
        self.tab_background_list = arcade.SpriteList()

        self.red = arcade.color.RED
        self.yellow = arcade.color.YELLOW
        self.green = arcade.color.GREEN

        self.aqua = arcade.color.AQUA
        self.azure = arcade.color.AZURE
        self.darkBlue = (0, 0, 139)

    def setup(self):
        """ Создает Ui обьекты"""
        self.health_bar = UltimateBar(
            max_value=self.game_state.player.health.max_health,
            current_value=self.game_state.player.health.current_health,
            center_x=400,
            center_y=530 - (15 / 4),
            width=200,
            height=15,
            color_left=self.red,
            color_mid=self.yellow,
            color_right=self.green,
            frame_texture_path="media/ui/hp_progressbar.png",
            is_gradient=True,
        )
        self.mana_bar = UltimateBar(
            max_value=self.game_state.player.mana.max_mana,
            current_value=self.game_state.player.mana.current_mana,
            center_x=400,
            center_y=570 + (15 / 4) - 20,
            width=200,
            height=15,
            color_left=self.darkBlue,
            color_mid=self.azure,
            color_right=self.aqua,
            frame_texture_path="media/ui/hp_progressbar.png",
            is_gradient=True,
        )

        self.health_bar.setup()
        self.mana_bar.setup()
        self.quickbar_texture = arcade.load_texture('media/ui/quickbar.png')
        self.slot_highlight_texture = arcade.load_texture("media/slot_highlight.png")

        # загрузка иконок
        for spell_id, spell_data in SPELL_DATA.items():
            try:
                self.spell_icons[spell_id] = arcade.load_texture(spell_data["icon"])
                print(f"Загружена иконка: {spell_id}")
            except Exception as e:
                print(f"Ошибка загрузки иконки {spell_id}: {e}")
                self.spell_icons[spell_id] = arcade.load_texture("media/placeholder_icon.png")

        # Созда7гите прицела
        crosshair_sprite = arcade.Sprite('media/staffs/crosshair.png', scale=1.0)
        crosshair_sprite.center_x = self.game_state.cursor_x
        crosshair_sprite.center_y = self.game_state.cursor_y
        self.crosshair_list.append(crosshair_sprite)

        # Создание прогрес бара
        progress_bar_y = 513
        slot_positions = [54, 118, 182, 246]
        for i in range(4):
            bar = SpellProgressBar(
                position=(slot_positions[i], progress_bar_y),
                size=(56, 8),
                frame_texture_path="media/ui/spell_progressbar.png"
            )
            self.spell_progress_bars.append(bar)

        # прогресс бар посоха
        # TODO доделать прогресс бар для посоха
        self.staff_cooldown_position = (400, 580)
        self.staff_cooldown_size = (100, 10)

        try:
            self.tab_background_sprite = arcade.Sprite('media/ui/Tab.png', scale=1.0)
            self.tab_background_sprite.center_x = SCREEN_WIDTH // 2
            self.tab_background_sprite.center_y = SCREEN_HEIGHT // 2
            self.tab_background_sprite.width = SCREEN_WIDTH
            self.tab_background_sprite.height = SCREEN_HEIGHT
            self.tab_background_list.append(self.tab_background_sprite)
            print("TAB загружен как спрайт")
        except FileNotFoundError:
            print("media/ui/Tab.png не найден")
            self.tab_background_sprite = None

    def update(self, delta_time):
        """ Логика обновления Ui"""
        if self.crosshair_list and len(self.crosshair_list) > 0:
            self.crosshair_list[0].center_x = self.game_state.cursor_x
            self.crosshair_list[0].center_y = self.game_state.cursor_y
        # обновляем прогресс бар
        if self.health_bar and self.game_state.player:
            self.health_bar.set_value(self.game_state.player.health.current_health)
        if self.mana_bar and self.game_state.player:
            self.mana_bar.set_value(self.game_state.player.mana.current_mana)
        # Обновление прогресс бара заклинний
        if self.game_state.spell_system:
            for i, spell in enumerate(self.game_state.spell_system.ready_spells):
                if i >= 4:
                    break

                if spell in self.game_state.spell_system.spell_reload_timers:
                    remaining = self.game_state.spell_system.spell_reload_timers[spell]
                    total = SPELL_DATA[spell]["reload_time"]
                    progress = 1.0 - (remaining / total) if total > 0 else 1.0
                    self.spell_progress_bars[i].set_progress(progress)
                else:
                    self.spell_progress_bars[i].set_progress(1.0)
            # Пустые слоты
            for i in range(len(self.game_state.spell_system.ready_spells), 4):
                self.spell_progress_bars[i].set_progress(0.0)

    def draw(self):
        """ Отрисовка Ui"""
        if self.game_state.elemental_circle:
            self.game_state.elemental_circle.draw(is_editing=self.game_state.is_tab_pressed)

        if self.health_bar:
            self.health_bar.draw()
        if self.mana_bar:
            self.mana_bar.draw()
        if self.game_state.show_fps:
            self.draw_fps()

        self.draw_quickbar()
        self.crosshair_list.draw()

        if self.game_state.is_tab_pressed and self.tab_background_sprite:
            self.tab_background_list.draw()
        elif self.game_state.is_tab_pressed:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                ),
                (0, 0, 0, 180)
            )

    def draw_quickbar(self):
        # отрисовка квик бара
        arcade.draw_texture_rect(self.quickbar_texture, arcade.rect.XYWH(150, 550, 256, 64), )

        # квик бар
        for i, spell in enumerate(self.game_state.spell_system.ready_spells):
            if i < 4:
                if spell in self.spell_icons:
                    texture = self.spell_icons[spell]
                    arcade.draw_texture_rect(
                        texture,
                        arcade.rect.XYWH(SLOT_POSITIONS[i][0], SLOT_POSITIONS[i][1], 48, 48)
                    )
        # подсветка иконок
        selected_index = self.game_state.spell_system.selected_spell_index
        if 0 <= selected_index < 4:
            highlight_x = SLOT_POSITIONS[selected_index][0]
            highlight_y = SLOT_POSITIONS[selected_index][1]
            arcade.draw_texture_rect(
                self.slot_highlight_texture,
                arcade.rect.XYWH(highlight_x, highlight_y, 64, 64)
            )
        # отрисовка прогресс бара
        for i, bar in enumerate(self.spell_progress_bars):
            if i < len(self.game_state.spell_system.ready_spells):
                bar.draw()  # рисуем только если слот занят

        # Рисуем прогресс-бар посоха
        if not self.game_state.can_shoot:
            progress = 1 - (self.game_state.shoot_timer / self.game_state.shoot_cooldown)
            bar_width = 100 * progress
            arcade.draw_rect_filled(
                arcade.rect.XYWH(400, 580, bar_width, 10),
                arcade.color.RED
            )

    def draw_fps(self):
        """ Метод для отрисовки фпс счетчика"""
        arcade.draw_text(
            str(self.game_state.current_fps),
            10, SCREEN_HEIGHT - 30,
            arcade.color.YELLOW,
            20,
            font_name='Minecraft Default'
        )
