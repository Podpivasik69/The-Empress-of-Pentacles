from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import arcade
import json
import os


class ElementalCircle:
    def __init__(self):
        self.bindings = self._load_bindings()  # загрузка биндов из json
        # малый круг
        self.sprite = arcade.Sprite('media/elemental_circle/Elemental_Diamond.png', scale=0.542)
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)
        # подсвеченная ячейка
        self.highlight_sprite = arcade.Sprite("media/slot_highlight.png", scale=0.5)
        self.highlight_list = arcade.SpriteList()
        self.highlight_list.append(self.highlight_sprite)
        # кеширование (оптимизация!)
        self.icon_rects_cache = {}

        self.sprite.center_x = SCREEN_WIDTH - 20 - self.sprite.width // 2
        self.sprite.center_y = SCREEN_HEIGHT - 20 - self.sprite.height // 2

        self.slot_rects = self._calculate_slot_rects()
        self.hovered_slot = None
        # картиночки стихий
        self.icons = {
            "fire": arcade.load_texture("media/elemental_circle/fire.png"),
            "water": arcade.load_texture("media/elemental_circle/water.png"),
            "earth": arcade.load_texture("media/elemental_circle/earth.png"),
            "air": arcade.load_texture("media/elemental_circle/air.png"),
            "empty": arcade.load_texture("media/elemental_circle/placeholder_icon.png")
        }

    def _load_bindings(self):
        # дефолт настройки
        default_bindings = {
            "UP": "fire",
            "LEFT": "water",
            "DOWN": None,
            "RIGHT": "earth",
        }
        # бинды
        filname = 'elemental_bindings.json'

        if os.path.exists(filname):
            try:
                with open(filname, 'r', encoding='utf8') as f:
                    loaded = json.load(f)
                    valid_keys = ['UP', "LEFT", 'DOWN', "RIGHT"]
                    for i in valid_keys:
                        if i in loaded and loaded[i] in ['fire', 'water', None]:
                            default_bindings[i] = loaded[i]
            except Exception as e:
                print(f'ошибка {filname}: {e}, были использованы дефолты')
        return default_bindings

    def _save_bindings(self):
        # сохры конфига в json
        try:
            with open('elemental_bindings.json', 'w', encoding='utf8') as f:
                json.dump(self.bindings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print('error {e}')

    def _calculate_slot_rects(self):
        center_x = self.sprite.center_x
        center_y = self.sprite.center_y

        # TODO убрать
        # print(f"DEBUG: center_x={center_x}, center_y={center_y}")

        button_size = 32
        offsets = {
            "UP": (0, button_size * 1.2),  # выше центра
            "DOWN": (0, -button_size * 1.2),  # ниже центра
            "LEFT": (-button_size * 1.2, 0),  # левее центра
            "RIGHT": (button_size * 1.2, 0),  # правее центра
        }

        rects = {}
        for direction, (dx, dy) in offsets.items():
            left = center_x + dx - button_size // 2
            bottom = center_y + dy - button_size // 2
            # TODO убрать
            # print(f"DEBUG: Creating rect at left={left}, bottom={bottom}, size={button_size}")
            rects[direction] = arcade.rect.XYWH(
                left + button_size // 2,  # center_x
                bottom + button_size // 2,  # center_y
                button_size,
                button_size
            )

        return rects

    def get_element(self, direction):
        # возвращени штучек
        return self.bindings.get(direction)

    def cycle_element(self, direction):
        # ролинг типо смение элемента по клику
        current = self.bindings.get(direction)
        cycle_order = ["fire", "water", "earth", None]  # огонь -> вода -> земля -> ПУСТО -> огонь

        if current in cycle_order:
            current_index = cycle_order.index(current)
            next_index = (current_index + 1) % len(cycle_order)
            self.bindings[direction] = cycle_order[next_index]
        else:
            self.bindings[direction] = "fire"
        self._save_bindings()
        return self.bindings[direction]

    def update_hover(self, x, y):
        # проверка через мышку
        self.hovered_slot = None
        for direction, rect in self.slot_rects.items():
            # если мышкой жмал
            left = rect.x - rect.width / 2
            right = rect.x + rect.width / 2
            bottom = rect.y - rect.height / 2
            top = rect.y + rect.height / 2

            if left <= x <= right and bottom <= y <= top:
                self.hovered_slot = direction
                break

    def draw(self, is_editing=False):
        # рисуем малую алхимическую пентограмму через SpriteList
        self.sprite_list.draw()

        center_x = self.sprite.center_x
        center_y = self.sprite.center_y
        icon_offsets = {
            "UP": (0, 38),  # 32 * 1.2 === 38
            "DOWN": (0, -38),
            "LEFT": (-38, 0),
            "RIGHT": (38, 0),
        }
        # иконки штучек
        for direction, (dx, dy) in icon_offsets.items():
            element = self.bindings.get(direction)
            icon_key = element if element in self.icons else "empty"
            texture = self.icons[icon_key]

            icon_x = center_x + dx
            icon_y = center_y + dy

            rect = arcade.rect.XYWH(icon_x, icon_y, 32, 32)
            arcade.draw_texture_rect(texture, rect)

        # подсветочка
        if is_editing and self.hovered_slot:
            dx, dy = icon_offsets[self.hovered_slot]
            self.highlight_sprite.center_x = center_x + dx
            self.highlight_sprite.center_y = center_y + dy

            self.highlight_list.draw()
