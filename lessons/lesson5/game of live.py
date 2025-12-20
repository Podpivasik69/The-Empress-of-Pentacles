import arcade
import random
import math
from enum import Enum

# Параметры экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
CELL_SIZE = 12  # Размер клетки

# Размеры сетки
GRID_WIDTH = 80  # SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = 60  # SCREEN_HEIGHT // CELL_SIZE


class PatternType(Enum):
    """Типы паттернов"""
    GLIDER = "Планер"
    GLIDER_GUN = "Ружьё Госпера"
    SPACESHIP = "Космический корабль"
    PULSAR = "Пульсар (осциллятор)"
    PENTADECATHLON = "Пентадекатлон"
    R_PENTOMINO = "R-пентамино (рост)"
    DIEHARD = "Диехард"
    ACORN = "Жёлудь"
    INFINITE_GROWTH = "Бесконечный рост"
    MAZE = "Лабиринт"
    FLOWER = "Цветок"
    FISH = "Рыба"
    CROSS = "Крест"


class RuleType(Enum):
    """Типы правил"""
    CLASSIC = "B3/S23"  # Классическая игра Жизнь
    HIGH_LIFE = "B36/S23"  # HighLife (репликатор)
    MAZE = "B3/S12345"  # Лабиринт
    MAZE_NO_S5 = "B3/S1234"  # Лабиринт без S5
    MAZE_MICE = "B37/S12345"  # Лабиринт с мышами
    MAZE_MICE2 = "B37/S1234"  # Mazectric with mice
    H_TREES = "B1/S012345678"  # H-деревья
    DIAMOEBA = "B35678/S5678"  # Диамёба
    ASSIMILATION = "B345/S4567"  # Ассимиляция
    DAY_NIGHT = "B3678/S34678"  # День и ночь
    CORAL = "B3/S45678"  # Кораллы
    AMOEBA = "B357/S1358"  # Амёба
    LIFE_34 = "B34/S34"  # 34 Жизнь
    SEEDS = "B2/S"  # Семена (B2/S0)
    DOTTED_LIFE = "B3/S023"  # Пунктирная жизнь


class GameOfLife(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Расширенная Игра Жизнь")
        arcade.set_background_color(arcade.color.BLACK)

        # Игровое поле
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.next_grid = None

        # Управление
        self.paused = True
        self.generation = 0
        self.update_speed = 0.05
        self.update_timer = 0

        # Текущее правило
        self.current_rule = RuleType.CLASSIC
        self.born_rules = [3]  # B правила (когда клетка рождается)
        self.survive_rules = [2, 3]  # S правила (когда клетка выживает)

        # Выбранный паттерн
        self.selected_pattern = PatternType.GLIDER
        self.patterns_loaded = False

        # Для отрисовки UI
        self.button_list = []
        self.pattern_buttons = []
        self.rule_buttons = []
        self.ui_elements = []

        # Цвета для разных состояний
        self.age_colors = [
            arcade.color.DARK_GREEN,
            arcade.color.GREEN,
            arcade.color.LIME_GREEN,
            arcade.color.YELLOW,
            arcade.color.GOLD,
            arcade.color.ORANGE,
            arcade.color.RED,
            arcade.color.DARK_RED,
            arcade.color.PURPLE,
            arcade.color.BLUE
        ]

        # Массив возраста клеток
        self.cell_age = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Флаг для рисования
        self.drawing = False
        self.erase_mode = False

    def setup(self):
        """Настройка игры"""
        self.create_ui()
        self.load_patterns()

    def create_ui(self):
        """Создание интерфейса"""
        self.button_list = []
        self.pattern_buttons = []
        self.rule_buttons = []
        self.ui_elements = []

        # Кнопки управления
        buttons_y = SCREEN_HEIGHT - 30
        button_width = 150

        # Паттерны (левая колонка)
        pattern_x = 10
        pattern_y = SCREEN_HEIGHT - 60
        pattern_labels = [
            ("Планер", PatternType.GLIDER),
            ("Ружьё Госпера", PatternType.GLIDER_GUN),
            ("Косм. корабль", PatternType.SPACESHIP),
            ("Пульсар", PatternType.PULSAR),
            ("Пентадекатлон", PatternType.PENTADECATHLON),
            ("R-пентамино", PatternType.R_PENTOMINO),
            ("Диехард", PatternType.DIEHARD),
            ("Жёлудь", PatternType.ACORN),
            ("Лабиринт", PatternType.MAZE),
            ("Цветок", PatternType.FLOWER)
        ]

        for i, (label, pattern) in enumerate(pattern_labels):
            y = pattern_y - i * 30
            btn = {"x": pattern_x, "y": y, "width": button_width, "height": 25,
                   "label": label, "pattern": pattern}
            self.pattern_buttons.append(btn)

        # Правила (правая колонка)
        rule_x = SCREEN_WIDTH - button_width - 10
        rule_y = SCREEN_HEIGHT - 60
        rule_labels = [
            ("Классика", RuleType.CLASSIC),
            ("HighLife", RuleType.HIGH_LIFE),
            ("Лабиринт", RuleType.MAZE),
            ("Лаб. без S5", RuleType.MAZE_NO_S5),
            ("Лаб. с мышами", RuleType.MAZE_MICE),
            ("Mazectric", RuleType.MAZE_MICE2),
            ("H-деревья", RuleType.H_TREES),
            ("Диамёба", RuleType.DIAMOEBA),
            ("Ассимиляция", RuleType.ASSIMILATION),
            ("День/ночь", RuleType.DAY_NIGHT),
            ("Кораллы", RuleType.CORAL),
            ("Амёба", RuleType.AMOEBA),
            ("34 Жизнь", RuleType.LIFE_34),
            ("Семена", RuleType.SEEDS)
        ]

        for i, (label, rule) in enumerate(rule_labels):
            y = rule_y - i * 25
            btn = {"x": rule_x, "y": y, "width": button_width, "height": 23,
                   "label": label, "rule": rule}
            self.rule_buttons.append(btn)

        # Кнопки управления внизу
        control_y = 40
        control_buttons = [
            ("C - Очистить", self.clear_grid),
            ("R - Случайно", self.random_fill),
            ("ПРОБЕЛ - Пауза", self.toggle_pause),
            ("E - Стереть", self.toggle_erase),
            ("1-9 - Скорость", None),
            ("ЛКМ - Рисовать", None),
            ("ПКМ - Удалить", None)
        ]

        for i, (label, _) in enumerate(control_buttons):
            x = 10 + i * 150
            if x + 140 < SCREEN_WIDTH:
                self.ui_elements.append({"type": "label", "x": x, "y": control_y, "text": label})

    def load_patterns(self):
        """Загрузка паттернов в словарь"""
        self.patterns = {}

        # Планер
        self.patterns[PatternType.GLIDER] = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]

        # Ружьё Госпера
        gun = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
             1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.patterns[PatternType.GLIDER_GUN] = gun

        # Легкий космический корабль
        self.patterns[PatternType.SPACESHIP] = [
            [0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0]
        ]

        # Пульсар (период 3)
        pulsar = []
        pattern = [
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
        ]
        self.patterns[PatternType.PULSAR] = pattern

        # R-пентамино (бесконечный рост)
        self.patterns[PatternType.R_PENTOMINO] = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 1, 0]
        ]

        # Диехард
        self.patterns[PatternType.DIEHARD] = [
            [0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1]
        ]

        # Жёлудь
        self.patterns[PatternType.ACORN] = [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1]
        ]

        # Простой лабиринт
        maze_pattern = []
        for i in range(15):
            row = []
            for j in range(15):
                if i == 0 or i == 14 or j == 0 or j == 14:
                    row.append(1)
                elif i % 2 == 0 and j % 2 == 0:
                    row.append(1)
                else:
                    row.append(0)
            maze_pattern.append(row)
        self.patterns[PatternType.MAZE] = maze_pattern

        # Цветок
        self.patterns[PatternType.FLOWER] = [
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0],
            [0, 0, 1, 0, 0]
        ]

        self.patterns_loaded = True

    def set_rule(self, rule_type):
        """Установка правила игры"""
        self.current_rule = rule_type

        if rule_type == RuleType.CLASSIC:
            self.born_rules = [3]
            self.survive_rules = [2, 3]
        elif rule_type == RuleType.HIGH_LIFE:
            self.born_rules = [3, 6]
            self.survive_rules = [2, 3]
        elif rule_type == RuleType.MAZE:
            self.born_rules = [3]
            self.survive_rules = [1, 2, 3, 4, 5]
        elif rule_type == RuleType.MAZE_NO_S5:
            self.born_rules = [3]
            self.survive_rules = [1, 2, 3, 4]
        elif rule_type == RuleType.MAZE_MICE:
            self.born_rules = [3, 7]
            self.survive_rules = [1, 2, 3, 4, 5]
        elif rule_type == RuleType.MAZE_MICE2:
            self.born_rules = [3, 7]
            self.survive_rules = [1, 2, 3, 4]
        elif rule_type == RuleType.H_TREES:
            self.born_rules = [1]
            self.survive_rules = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        elif rule_type == RuleType.DIAMOEBA:
            self.born_rules = [3, 5, 6, 7, 8]
            self.survive_rules = [5, 6, 7, 8]
        elif rule_type == RuleType.ASSIMILATION:
            self.born_rules = [3, 4, 5]
            self.survive_rules = [4, 5, 6, 7]
        elif rule_type == RuleType.DAY_NIGHT:
            self.born_rules = [3, 6, 7, 8]
            self.survive_rules = [3, 4, 6, 7, 8]
        elif rule_type == RuleType.CORAL:
            self.born_rules = [3]
            self.survive_rules = [4, 5, 6, 7, 8]
        elif rule_type == RuleType.AMOEBA:
            self.born_rules = [3, 5, 7]
            self.survive_rules = [1, 3, 5, 8]
        elif rule_type == RuleType.LIFE_34:
            self.born_rules = [3, 4]
            self.survive_rules = [3, 4]
        elif rule_type == RuleType.SEEDS:
            self.born_rules = [2]
            self.survive_rules = []

    def clear_grid(self):
        """Очистка поля"""
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                self.grid[row][col] = 0
                self.cell_age[row][col] = 0
        self.generation = 0

    def random_fill(self, density=0.3):
        """Случайное заполнение"""
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                self.grid[row][col] = 1 if random.random() < density else 0
                if self.grid[row][col] == 1:
                    self.cell_age[row][col] = 1
                else:
                    self.cell_age[row][col] = 0
        self.generation = 0

    def place_pattern(self, pattern_type, center_x=None, center_y=None):
        """Размещение паттерна на поле"""
        if pattern_type not in self.patterns:
            return

        pattern = self.patterns[pattern_type]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if center_x is None:
            center_x = GRID_WIDTH // 2
        if center_y is None:
            center_y = GRID_HEIGHT // 2

        start_x = center_x - pattern_width // 2
        start_y = center_y - pattern_height // 2

        for y in range(pattern_height):
            for x in range(pattern_width):
                grid_x = start_x + x
                grid_y = start_y + y

                if (0 <= grid_x < GRID_WIDTH and
                        0 <= grid_y < GRID_HEIGHT and
                        pattern[y][x] == 1):
                    self.grid[grid_y][grid_x] = 1
                    self.cell_age[grid_y][grid_x] = 1

    def count_neighbors(self, row, col):
        """Подсчёт соседей с тороидальными границами"""
        count = 0

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr = (row + dr) % GRID_HEIGHT
                nc = (col + dc) % GRID_WIDTH

                if self.grid[nr][nc] == 1:
                    count += 1

        return count

    def update_grid(self):
        """Обновление состояния поля по текущим правилам"""
        self.next_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        next_age = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                neighbors = self.count_neighbors(row, col)
                current_state = self.grid[row][col]
                current_age = self.cell_age[row][col]

                if current_state == 1:
                    # Клетка жива - проверяем выживание
                    if neighbors in self.survive_rules:
                        self.next_grid[row][col] = 1
                        next_age[row][col] = min(current_age + 1, len(self.age_colors) - 1)
                    else:
                        self.next_grid[row][col] = 0
                        next_age[row][col] = 0
                else:
                    # Клетка мертва - проверяем рождение
                    if neighbors in self.born_rules:
                        self.next_grid[row][col] = 1
                        next_age[row][col] = 1
                    else:
                        self.next_grid[row][col] = 0
                        next_age[row][col] = 0

        self.grid = self.next_grid
        self.cell_age = next_age
        self.generation += 1

    def toggle_pause(self):
        """Переключение паузы"""
        self.paused = not self.paused

    def toggle_erase(self):
        """Переключение режима стирания"""
        self.erase_mode = not self.erase_mode

    def on_draw(self):
        """Отрисовка игры"""
        self.clear()

        # Рисуем клетки с цветом по возрасту
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col] == 1:
                    x = col * CELL_SIZE + CELL_SIZE // 2
                    y = row * CELL_SIZE + CELL_SIZE // 2

                    # Цвет зависит от возраста клетки
                    age = self.cell_age[row][col]
                    color_index = min(age, len(self.age_colors) - 1)
                    color = self.age_colors[color_index]

                    # Рисуем клетку
                    arcade.draw_rect_filled(
                        arcade.rect.XYWH(x, y, CELL_SIZE - 1, CELL_SIZE - 1),
                        color
                    )

                    # Контур для старых клеток
                    if age > 5:
                        arcade.draw_rect_outline(
                            arcade.rect.XYWH(x, y, CELL_SIZE - 1, CELL_SIZE - 1),
                            arcade.color.WHITE,
                            1
                        )

        # Рисуем сетку
        for row in range(GRID_HEIGHT + 1):
            y = row * CELL_SIZE
            arcade.draw_line(0, y, GRID_WIDTH * CELL_SIZE, y, arcade.color.GRAY)
        for col in range(GRID_WIDTH + 1):
            x = col * CELL_SIZE
            arcade.draw_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, arcade.color.GRAY)

        # Рисуем UI элементы
        self.draw_ui()

    def draw_ui(self):
        """Отрисовка интерфейса"""
        # Информация о состоянии
        status_color = arcade.color.RED if self.paused else arcade.color.GREEN
        status_text = "ПАУЗА" if self.paused else "ИДЁТ"

        arcade.draw_text(f"Состояние: {status_text}", 10, SCREEN_HEIGHT - 25,
                         status_color, 16, bold=True)
        arcade.draw_text(f"Поколение: {self.generation}", 10, SCREEN_HEIGHT - 45,
                         arcade.color.WHITE, 14)
        arcade.draw_text(f"Правило: {self.current_rule.value}", 10, SCREEN_HEIGHT - 65,
                         arcade.color.CYAN, 14)
        arcade.draw_text(f"Паттерн: {self.selected_pattern.value}", 10, SCREEN_HEIGHT - 85,
                         arcade.color.YELLOW, 14)
        arcade.draw_text(f"Режим: {'СТИРАНИЕ' if self.erase_mode else 'РИСОВАНИЕ'}",
                         10, SCREEN_HEIGHT - 105,
                         arcade.color.ORANGE if self.erase_mode else arcade.color.LIME, 14)

        # Кнопки паттернов
        for btn in self.pattern_buttons:
            color = arcade.color.BLUE_GRAY
            if self.selected_pattern == btn["pattern"]:
                color = arcade.color.GOLD

            # Фон кнопки
            arcade.draw_lrbt_rectangle_filled(  # вариант 2: лево, право, низ, верх
                btn["x"],
                btn["x"] + btn["width"],
                btn["y"] - btn["height"],
                btn["y"],
                color
            )

            # Текст кнопки
            arcade.draw_text(
                btn["label"],
                btn["x"] + 5,
                btn["y"] - btn["height"] + 5,
                arcade.color.WHITE,
                12
            )

            # Рамка
            arcade.draw_lbwh_rectangle_outline(
                btn["x"], btn["y"] - btn["height"],
                btn["width"], btn["height"],
                arcade.color.WHITE,
                1
            )

        # Кнопки правил
        for btn in self.rule_buttons:
            color = arcade.color.DARK_SLATE_GRAY
            if self.current_rule == btn["rule"]:
                color = arcade.color.DARK_GREEN

            # Фон кнопки
            arcade.draw_lrbt_rectangle_filled(  # вариант 2: лево, право, низ, верх
                btn["x"],
                btn["x"] + btn["width"],
                btn["y"] - btn["height"],
                btn["y"],
                color
            )

            # Текст кнопки
            arcade.draw_text(
                btn["label"],
                btn["x"] + 5,
                btn["y"] - btn["height"] + 5,
                arcade.color.WHITE,
                10
            )

            # Рамка
            arcade.draw_lbwh_rectangle_outline(
                btn["x"], btn["y"] - btn["height"],
                btn["width"], btn["height"],
                arcade.color.WHITE,
                1
            )

        # Управление внизу
        for element in self.ui_elements:
            arcade.draw_text(
                element["text"],
                element["x"],
                element["y"],
                arcade.color.LIGHT_GRAY,
                12
            )

    def on_update(self, delta_time):
        """Обновление игры"""
        if self.paused:
            return

        self.update_timer += delta_time
        if self.update_timer >= self.update_speed:
            self.update_timer = 0
            self.update_grid()

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка кликов мыши"""
        # Проверяем клик по кнопкам паттернов
        for btn in self.pattern_buttons:
            if (btn["x"] <= x <= btn["x"] + btn["width"] and
                    btn["y"] - btn["height"] <= y <= btn["y"]):
                self.selected_pattern = btn["pattern"]
                self.place_pattern(btn["pattern"])
                return

        # Проверяем клик по кнопкам правил
        for btn in self.rule_buttons:
            if (btn["x"] <= x <= btn["x"] + btn["width"] and
                    btn["y"] - btn["height"] <= y <= btn["y"]):
                self.set_rule(btn["rule"])
                return

        # Рисование на поле
        if 0 <= x < GRID_WIDTH * CELL_SIZE and 0 <= y < GRID_HEIGHT * CELL_SIZE:
            col = int(x // CELL_SIZE)
            row = int(y // CELL_SIZE)

            if button == arcade.MOUSE_BUTTON_LEFT:
                if modifiers & arcade.key.MOD_SHIFT:
                    # Shift+ЛКМ - разместить выбранный паттерн
                    self.place_pattern(self.selected_pattern, col, row)
                else:
                    # Обычный ЛКМ - рисование/стирание
                    self.drawing = True
                    self.grid[row][col] = 0 if self.erase_mode else 1
                    if not self.erase_mode:
                        self.cell_age[row][col] = 1
            elif button == arcade.MOUSE_BUTTON_RIGHT:
                # ПКМ - стирание
                self.grid[row][col] = 0
                self.cell_age[row][col] = 0

    def on_mouse_release(self, x, y, button, modifiers):
        """Обработка отпускания кнопки мыши"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.drawing = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Обработка перетаскивания мыши"""
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            if 0 <= x < GRID_WIDTH * CELL_SIZE and 0 <= y < GRID_HEIGHT * CELL_SIZE:
                col = int(x // CELL_SIZE)
                row = int(y // CELL_SIZE)

                if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                    self.grid[row][col] = 0 if self.erase_mode else 1
                    if not self.erase_mode:
                        self.cell_age[row][col] = 1

    def on_key_press(self, key, modifiers):
        """Обработка нажатия клавиш"""
        if key == arcade.key.SPACE:
            self.toggle_pause()
        elif key == arcade.key.C:
            self.clear_grid()
        elif key == arcade.key.R:
            self.random_fill()
        elif key == arcade.key.E:
            self.toggle_erase()
        elif key == arcade.key.G:
            # Автоматическая генерация интересных конфигураций
            self.generate_interesting_config()
        elif arcade.key.KEY_1 <= key <= arcade.key.KEY_9:
            # Установка скорости 1-9
            speed_index = key - arcade.key.KEY_1
            speeds = [0.5, 0.2, 0.1, 0.05, 0.03, 0.02, 0.015, 0.01, 0.005]
            self.update_speed = speeds[speed_index]
        elif key == arcade.key.P:
            # Сохранить текущее состояние
            self.save_snapshot()
        elif key == arcade.key.L:
            # Загрузить сохранённое состояние
            self.load_snapshot()

    def generate_interesting_config(self):
        """Генерация интересной конфигурации"""
        self.clear_grid()

        # Случайный выбор типа генерации
        gen_type = random.choice(["maze", "guns", "oscillators", "symmetric", "chaos"])

        if gen_type == "maze":
            self.set_rule(random.choice([
                RuleType.MAZE, RuleType.MAZE_NO_S5,
                RuleType.MAZE_MICE, RuleType.MAZE_MICE2
            ]))
            self.random_fill(0.4)

        elif gen_type == "guns":
            self.set_rule(RuleType.CLASSIC)
            # Размещаем несколько ружей Госпера
            for i in range(random.randint(2, 4)):
                x = random.randint(10, GRID_WIDTH - 36)
                y = random.randint(10, GRID_HEIGHT - 10)
                self.place_pattern(PatternType.GLIDER_GUN, x, y)

        elif gen_type == "oscillators":
            self.set_rule(RuleType.CLASSIC)
            # Размещаем осцилляторы
            patterns = random.sample([
                PatternType.PULSAR, PatternType.PENTADECATHLON,
                PatternType.FLOWER, PatternType.CROSS
            ], random.randint(2, 3))

            for i, pattern in enumerate(patterns):
                x = GRID_WIDTH // 4 + i * (GRID_WIDTH // 4)
                y = GRID_HEIGHT // 2
                self.place_pattern(pattern, x, y)

        elif gen_type == "symmetric":
            # Симметричный узор
            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH // 2):
                    if random.random() < 0.2:
                        self.grid[row][col] = 1
                        self.grid[row][GRID_WIDTH - col - 1] = 1

        elif gen_type == "chaos":
            # Хаотичное заполнение с интересным правилом
            interesting_rules = [
                RuleType.DIAMOEBA, RuleType.ASSIMILATION,
                RuleType.DAY_NIGHT, RuleType.AMOEBA
            ]
            self.set_rule(random.choice(interesting_rules))
            self.random_fill(0.25)

    def save_snapshot(self):
        """Сохранение снимка состояния (упрощённая версия)"""
        print("Снимок сохранён (в памяти)")
        # В реальном приложении здесь можно сохранять в файл

    def load_snapshot(self):
        """Загрузка снимка состояния (упрощённая версия)"""
        print("Загружен последний снимок")
        # В реальном приложении здесь можно загружать из файла


def main():
    """Главная функция"""
    game = GameOfLife()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
