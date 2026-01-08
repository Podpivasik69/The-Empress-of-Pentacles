# SpellManager
from core.entity_manager import EntityManager
import arcade
from core.game_state import GameState
from core.spell_factory import create_spell


class SpellManager:
    def __init__(self, game_state, entity_manager):
        self.game_state = game_state
        self.entity_manager = entity_manager
        # список для хранения заклинаний
        self.active_spells = []

    def create_shoot(self, spell_id, start_x, start_y, target_x, target_y):
        spell = create_spell(spell_id, start_x, start_y, target_x, target_y, self.entity_manager)  # создаем заклинания через фабрику
        # если заклинание недействительное то сбрасываем
        if spell is None:
            print(f'ошибка создания закнинания {spell_id}')
            return
            # добавляем в список заклинаний
        self.active_spells.append(spell)

    def update(self, delta_time):
        # обновляем все заклинания
        for spell in self.active_spells:
            if spell is not None:
                spell.update(delta_time)
                # проверяем жив ли снаряд
                if spell.is_alive:
                    pass
                    # проверка на коллизию
                    # spell.check_collisions(self.entity_manager.enemy_sprites)

        self.remove_dead_sells()

    def draw(self):
        """ Просто рисуем все заклинания"""
        for spell in self.active_spells:
            spell.draw()

    def remove_dead_sells(self):
        """ Удаляем список мертвых клеток мозга.... тоесть заклинания"""
        # список живых заклинаний в данный момент
        alive_spells = []
        for spell in self.active_spells:
            # если флаг заклинания - is_alive то добавляем в список живых заклинаний
            if spell.is_alive:
                alive_spells.append(spell)
        self.active_spells = alive_spells
