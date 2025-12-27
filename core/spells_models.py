from constants import *


class BaseSpell:
    def __init__(self, start_x, start_y, target_x, target_y, spell_type, is_alive):
        # начальная позиция снаряда (кончик посоха, над головой, или вообще без точки стара, просто появление в нужной точке)
        self.start_x = start_x
        self.start_y = start_y
        # конечная позиция снаряда (обычно это курсор, но для некоторых может менятся в замосимости от логики
        # например заклинания с самонаведением
        self.target_x = target_x
        self.target_y = target_y
        # тип заклинания - балистические, статические, и тд
        self.spell_type = spell_type
        # живо ли заклинание? наверное нужно для того чтобы удалить заклинание после условия, например после попадания или через время
        self.is_alive = is_alive

    def update(self, delta_time):
        """ Переопределить потом"""
        raise NotImplementedError('реализовать update')

    def draw(self):
        """ Переопределить потом"""
        raise NotImplementedError('реализовать draw')

    def check_collisions(self, enemies):
        """ Переопределить потом"""
        raise NotImplementedError('реализовать check_collisions')

    def should_remove(self):
        """ Когда стоит удалять заклинение?"""
        return not self.is_alive
