from staff import BASIC_STAFF
import arcade
from elemental_circle import *


class SpellSystem:
    def __init__(self, elemental_circle):
        self.elemental_circle = elemental_circle
        # стрелять
        self.spell_combo = []  # список комбинаций клавишь
        self.combo_timer = 0.0
        self.is_ready_to_fire = False  # хочу выстрел хочу выстрел хочу выстрел
        self.spells_list = []
        self.casted_spell = None  # текущее скастованое заклинание
        self.ready_spells = []  # список скастованых готовых к стрельбе заклинаний
        self.max_spell = 3  # пока что можно делать заклинания из 3 стихий
        self.selected_spell_index = -1  # 0-3 это у нас 1-4 слоты. -1 = ничего не выбрано
        self.active_spell = None  # выбранное заклинание
        # self.shoot_cooldown = 0.5  # время на перезарядку посоха
        self.spell_reload_timers = {}  # кароче словарь для соответствия заклинаний и их времени кд
        self.spell_ready = set()  # готовые заклинания

    def setup(self):
        pass

    def add_to_combo(self, direction):
        if len(self.spell_combo) < self.max_spell:
            self.spell_combo.append(direction)
            return True
        return False

    def create_spell_from_combo(self):
        if not self.spell_combo:
            return None

        combo_length = len(self.spell_combo)
        first_element = self.spell_combo[0]

        # определения типа стихии по первому элементу из каста
        # измено - определении типа стихии по алхимическому кругу
        element = self.elemental_circle.get_element(first_element)
        if element is None:
            return None
        spell_name = None

        if element == "fire":
            if combo_length == 1:
                spell_name  = "fire_spark"
            elif combo_length == 2:
                spell_name  = "fireball"
            elif combo_length == 3:
                spell_name  = "sun_strike"
        if element == "water":
            if combo_length == 1:
                spell_name  = "splashing_water"
            elif combo_length == 2:
                spell_name  = "waterball"
            elif combo_length == 3:
                spell_name  = "water_cannon"

        if spell_name:
            print(f'создано новое заклинание {spell_name}')
            self.casted_spell = spell_name
            self.is_ready_to_fire = True
            self.spell_combo = []
            self.combo_timer = 0.0
            return spell_name
        return None

    def add_spell_to_quickbar(self, spell_name):
        if spell_name is None:
            return False
        if len(self.ready_spells) < 4:
            if spell_name not in self.ready_spells:
                self.ready_spells.append(spell_name)
                self.spell_ready.add(spell_name)
                print(
                    f'в квик бар добавлено заклинание {spell_name} занято {len(self.ready_spells)} слотов')

                return True
            else:
                print(f'спел {spell_name} уже есть в квикбаре!')
                return False

        else:
            print("квикбар полон. макс 4 спела")
            return False
