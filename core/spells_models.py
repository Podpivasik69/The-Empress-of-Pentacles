# core/spells_models.py
import arcade

from constants import *
import math


class BaseSpell:
    def __init__(self, spell_name, start_x, start_y, target_x, target_y, spell_type, is_alive=True):
        # название заклинания
        self.spell_name = spell_name
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
        # текущие координаты заклинания
        self.x = start_x
        self.y = start_y
        # словарь с всеми данными об заклинаниии
        self.data = SPELL_DATA[spell_name]

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


class LinearProjectileSpell(BaseSpell):
    """ Класс для заклинаний имеющих линейную траэкторию полета """

    def __init__(self, spell_id, start_x, start_y, target_x, target_y):
        super().__init__(spell_id, start_x, start_y, target_x, target_y, 'linear_projectile', True)
        self.speed = self.data['speed']
        self.piercing = self.data.get('piercing', False)
        # создаем спрайт, если в словаре нет текстуры, берем заглушку
        sprite_path = self.data['game_sprite']
        if not sprite_path:
            sprite_path = 'media/placeholder_icon.png'
        self.sprite = arcade.Sprite(sprite_path)
        # создаем список спрайтов для заклинания, добавляем в него заклинание
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        # насколько цель правее старта
        # если dx > 0 - цель правее
        # если dx < 0 цель левее
        # если dx = 0 цель вертикально относительно нас
        dx = self.target_x - self.start_x
        # насколько цель выше старта
        # если dy > 0 - цель выше
        # если dy < 0 цель ниже
        # если dy = 0 цель горизонтально относительно нас
        dy = self.target_y - self.start_y
        # расчет угла между горизонтальной осью и вектором dx dy
        launch_angle = math.atan2(dy, dx)
        # вертора направление x/y
        self.direction_x = math.cos(launch_angle)
        self.direction_y = math.sin(launch_angle)

    def update(self, delta_time):
        move_x = self.direction_x * self.speed * delta_time
        move_y = self.direction_y * self.speed * delta_time

        self.x += move_x
        self.y += move_y

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def draw(self):
        self.sprite_list.draw()

    # TODO сделать коллизию не только с врагами
    def check_collisions(self, enemies):
        """ Метод для проверки колизии между заклинанием и врагом"""
        # проверка на сталкновение через встроенную функцию аркейд
        # она возвращает список спрайтов врагов, с которыми столкнулся снаряд
        hit_sprites = arcade.check_for_collision_with_list(self.sprite, enemies)
        # если нет столкновений возвращаем пустой список
        if not hit_sprites:
            return []
        # список для хранения обьектов поражанных врагов
        collisions_enemies = []
        # перебираем каждого пораженного врага
        for enemy_sprite in hit_sprites:
            # получаем обьект врага из его спрайта через функциб enemy_object которая возвращает сам обьект
            enemy = enemy_sprite.enemy_object

            if not enemy.is_alive:
                # пропускаем мертвых врагов
                continue

            # отнимаем здоровье врага, равное количеству урона в словаря текущего заклинания
            enemy.take_damage(self.data.get('damage'))
            print(f"враг {enemy.__class__.__name__} получил {self.data.get('damage')} урона")
            print(f"у врага {enemy.__class__.__name__} осталось еще {enemy.health.current_health} ")
            # добавляем врага в список пораженных
            collisions_enemies.append(enemy)
        # если заклинание не пробивающее, то оно удалится об врага, если пробивающее то вылетит насквось
        if not self.piercing:
            self.is_alive = False
        # возвращаем список обьектов пораженных врагов
        return collisions_enemies


class FireSparkSpell(LinearProjectileSpell):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__('fire_spark', start_x, start_y, target_x, target_y)


class WaterSplashingSpell(LinearProjectileSpell):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__('splashing_water', start_x, start_y, target_x, target_y)


class ParabolicProjectileSpell(BaseSpell):
    """ Класс для заклинаний имеющих параболическую траекторию полета """

    def __init__(self, spell_id, start_x, start_y, target_x, target_y):
        super().__init__(spell_id, start_x, start_y, target_x, target_y, 'parabolic_projectile', True)
        self.speed = self.data['speed']
        self.gravity = self.data['gravity']
        self.exponent = self.data.get('gravity_exponent', 1.5)

        self.rotates = self.data.get('rotates', False)
        self.velocity_x = 0
        self.velocity_y = 0

        # создаем спрайт, если в словаре нет текстуры, берем заглушку
        sprite_path = self.data['game_sprite']
        if not sprite_path:
            sprite_path = 'media/placeholder_icon.png'
        self.sprite = arcade.Sprite(sprite_path)
        # создаем список спрайтов для заклинания, добавляем в него заклинание
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.sprite)

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        # насколько цель правее старта
        # если dx > 0 - цель правее
        # если dx < 0 цель левее
        # если dx = 0 цель вертикально относительно нас
        dx = self.target_x - self.start_x
        # насколько цель выше старта
        # если dy > 0 - цель выше
        # если dy < 0 цель ниже
        # если dy = 0 цель горизонтально относительно нас
        dy = self.target_y - self.start_y
        # расчет угла между горизонтальной осью и вектором dx dy
        launch_angle = math.atan2(dy, dx)
        # вертора направление x/y
        self.direction_x = math.cos(launch_angle)
        self.direction_y = math.sin(launch_angle)

        self.timer = 0.0

    def update(self, delta_time):
        self.timer += delta_time
        move_x = self.direction_x * self.speed * delta_time
        move_y = (self.direction_y * self.speed * delta_time) - (self.gravity / 100 * (self.timer ** self.exponent))

        self.x += move_x
        self.y += move_y

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def draw(self):
        self.sprite_list.draw()

    # TODO сделать коллизию не только с врагами
    def check_collisions(self, enemies):
        """ Метод для проверки колизии между заклинанием и врагом"""
        # проверка на сталкновение через встроенную функцию аркейд
        # она возвращает список спрайтов врагов, с которыми столкнулся снаряд
        hit_sprites = arcade.check_for_collision_with_list(self.sprite, enemies)
        # если нет столкновений возвращаем пустой список
        if not hit_sprites:
            return []
        # список для хранения обьектов поражанных врагов
        collisions_enemies = []
        # перебираем каждого пораженного врага
        for enemy_sprite in hit_sprites:
            # получаем обьект врага из его спрайта через функциб enemy_object которая возвращает сам обьект
            enemy = enemy_sprite.enemy_object

            if not enemy.is_alive:
                # пропускаем мертвых врагов
                continue

            # отнимаем здоровье врага, равное количеству урона в словаря текущего заклинания
            enemy.take_damage(self.data.get('damage'))
            print(f"враг {enemy.__class__.__name__} получил {self.data.get('damage')} урона")
            print(f"у врага {enemy.__class__.__name__} осталось еще {enemy.health.current_health} ")
            # добавляем врага в список пораженных
            collisions_enemies.append(enemy)
        # если заклинание не пробивающее, то оно удалится об врага, если пробивающее то вылетит насквось
        if not self.data.get('piercing', False):
            self.is_alive = False
        # возвращаем список обьектов пораженных врагов
        return collisions_enemies


class FireBallSpell(ParabolicProjectileSpell):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__('fireball', start_x, start_y, target_x, target_y)


class WaterBallSpell(ParabolicProjectileSpell):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__('waterball', start_x, start_y, target_x, target_y)


class AreaSpell(BaseSpell):
    """ Класс для заклинаний в определенной точке / области """

    def __init__(self, spell_id, target_x, target_y):
        super().__init__(spell_id, None, None, target_x, target_y, 'area_spell', True)
        self.data = SPELL_DATA[spell_id]  # словарь заклинания
        self.delay_to_cast = self.data.get('delay_to_cast', 0.0)  # задержка заклинания перед появлением
        # задержка (между нажатием лкм и появлением)
        self.radius = self.data.get('radius', 100)  # радиус поражения заклинания (может быть больше или меньше спрайта)
        self.piercing = self.data.get('piercing', True)  # пробитие
        self.damage_frame = self.data.get('damage_frame', 1)  # кадр анимации на котором наносится урон

        self.total_frames = self.data.get('total_frames', None)  # всего кадров
        self.current_frame = 0  # текущий кадр
        self.frame_list = arcade.SpriteList()
        self.timer = 0.0

        path_template = self.data.get('frame_path', 'media/ui/place_holder.png')
        for frame in range(self.total_frames):
            frame_path = path_template.format(frame)
            sprite = arcade.Sprite(frame_path)
            self.frame_list.append(sprite)

    def update(self, delta_time):
        self.timer += delta_time
        self.current_frame += 1

    def draw(self):
        self.frame_list.draw()

    def check_collisions(self, enemies):
        """ Метод для проверки колизии между заклинанием и врагом"""
        # проверка на сталкновение через встроенную функцию аркейд
        # она возвращает список спрайтов врагов, с которыми столкнулся снаряд
        hit_sprites = arcade.check_for_collision_with_list(enemies, self.frame_list)
        # если нет столкновений возвращаем пустой список
        if not hit_sprites:
            return []
        # список для хранения обьектов поражанных врагов
        collisions_enemies = []
        # перебираем каждого пораженного врага
        for enemy_sprite in hit_sprites:
            # получаем обьект врага из его спрайта через функциб enemy_object которая возвращает сам обьект
            enemy = enemy_sprite.enemy_object

            if not enemy.is_alive:
                # пропускаем мертвых врагов
                continue

            # отнимаем здоровье врага, равное количеству урона в словаря текущего заклинания
            enemy.take_damage(self.data.get('damage'))
            print(f"враг {enemy.__class__.__name__} получил {self.data.get('damage')} урона")
            print(f"у врага {enemy.__class__.__name__} осталось еще {enemy.health.current_health} ")
            # добавляем врага в список пораженных
            collisions_enemies.append(enemy)
        # если заклинание не пробивающее, то оно удалится об врага, если пробивающее то вылетит насквось
        if not self.data.get('piercing', False):
            self.is_alive = False
        # возвращаем список обьектов пораженных врагов
        return collisions_enemies


class SunStrikeSpell(AreaSpell):
    def __init__(self, target_x, target_y):
        super().__init__('sun_strike', target_x, target_y)
