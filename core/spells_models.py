# core/spells_models.py
from constants import *
from core.camera_manager import CameraManager
from core.game_state import GameState
import arcade
import math


class BaseSpell:
    def __init__(self, spell_name, start_world_x, start_world_y, target_world_x,
                 target_world_y, spell_type, is_alive=True):
        # название заклинания
        self.spell_name = spell_name

        # тип заклинания - балистические, статические, и тд
        self.spell_type = spell_type

        # начальная позиция снаряда в мировых координатах
        # (кончик посоха, над головой, или вообще без точки стара, просто появление в нужной точке)
        self.start_world_x = start_world_x
        self.start_world_y = start_world_y
        # конечная позиция снаряда в мировых координатах
        # (обычно это курсор, но для некоторых может менятся в замосимости от логики например заклинания с самонаведением)
        self.target_world_x = target_world_x
        self.target_world_y = target_world_y

        # экранные кооринаты для отрисовки
        self.screen_x = 0
        self.screen_y = 0

        # текущие мировые координаты заклинания
        self.world_x = start_world_x
        self.world_y = start_world_y

        # живо ли заклинание? наверное нужно для того чтобы удалить заклинание после условия, например после попадания или через время
        self.is_alive = is_alive
        # словарь с всеми данными об заклинаниии
        self.data = SPELL_DATA[spell_name]
        self.game_state = None

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

    def set_game_state(self, game_state):
        self.game_state = game_state

    def world_to_screen(self, world_x=None, world_y=None):
        """ мироыве координаты в экранные"""
        if world_x is None:
            world_x = self.world_x
        if world_y is None:
            world_y = self.world_y

        if self.game_state and self.game_state.camera_manager:
            # через camera manager
            return self.game_state.camera_manager.world_to_screen(world_x, world_y)
        else:
            return world_x, world_y


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

        self.sprite.center_x = self.world_x
        self.sprite.center_y = self.world_y

        # насколько цель правее старта
        # если dx > 0 - цель правее
        # если dx < 0 цель левее
        # если dx = 0 цель вертикально относительно нас
        dx = self.target_world_x - self.start_world_x
        # насколько цель выше старта
        # если dy > 0 - цель выше
        # если dy < 0 цель ниже
        # если dy = 0 цель горизонтально относительно нас
        dy = self.target_world_y - self.start_world_y
        # расчет угла между горизонтальной осью и вектором dx dy
        launch_angle = math.atan2(dy, dx)
        # вертора направление x/y
        self.direction_x = math.cos(launch_angle)
        self.direction_y = math.sin(launch_angle)

    def update(self, delta_time):
        move_x = self.direction_x * self.speed * delta_time
        move_y = self.direction_y * self.speed * delta_time

        self.world_x += move_x
        self.world_y += move_y

        screen_x, screen_y = self.world_to_screen(self.world_x, self.world_y)

        self.sprite.center_x = screen_x
        self.sprite.center_y = screen_y

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

    def __init__(self, spell_id, target_x, target_y, entity_manager=None):
        super().__init__(spell_id, None, None, target_x, target_y, 'area_spell', True)
        self.data = SPELL_DATA[spell_id]  # словарь заклинания
        self.entity_manager = entity_manager
        self.delay_to_cast = self.data.get('delay_to_cast', 0.0)  # задержка заклинания перед появлением
        # /|\
        #  |
        # задержка (между нажатием лкм и появлением)
        # базовые размеры и маштаб
        self.base_width = self.data.get('base_width', 100)
        self.base_height = self.data.get('base_height', 100)
        self.sprite_scale = self.data.get('sprite_scale', 1.0)
        # актуальные размеры
        self.hitbox_width = self.base_width * self.sprite_scale
        self.hitbox_height = self.base_height * self.sprite_scale

        self.piercing = self.data.get('piercing', True)  # пробитие
        # self.damage_frame = self.data.get('damage_frame', 1)  # кадр анимации на котором наносится урон
        self.frame_duration = self.data.get('frame_duration', 0.1)  # задержка между каждрами, в секундах
        self.total_frames = self.data.get('total_frames', None)  # всего кадров
        self.current_frame = 0  # текущий кадр
        # self.damage_dealt = False  # флаг - нанесен ли урон?

        self.frame_list = arcade.SpriteList()
        self.current_sprite = None
        self.timer = 0.0

        self.draw_list = arcade.SpriteList()

        path_template = self.data.get('frame_path', 'media/ui/place_holder.png')
        for frame in range(self.total_frames):
            frame_path = path_template.format(frame)
            sprite = arcade.Sprite(frame_path, scale=self.sprite_scale)

            sprite.center_x = target_x
            sprite.center_y = target_y
            self.frame_list.append(sprite)

    def update(self, delta_time):
        # пока есть задержка, отнимаем ее, не начинем анимацию
        if self.delay_to_cast > 0:
            self.delay_to_cast -= delta_time  # тупо вычитаем время из задержки пока она не закончилась
            return

        self.timer += delta_time
        # увеличиваем кадр анимации на основе времени
        self.current_frame = int(self.timer / self.frame_duration)

        if self.current_frame < self.total_frames:
            self.current_sprite = self.frame_list[self.current_frame]
            self.check_and_apply_damage()


        else:
            self.is_alive = False

    def draw(self):
        if self.current_sprite:
            temp_list = arcade.SpriteList()
            temp_list.append(self.current_sprite)
            temp_list.draw()

    # def check_collisions(self, enemies):
    #     """ Метод для проверки колизии между заклинанием и врагом"""
    #     # проверка на сталкновение через встроенную функцию аркейд
    #     # она возвращает список спрайтов врагов, с которыми столкнулся снаряд
    #     hit_sprites = arcade.check_for_collision_with_list(enemies, self.frame_list)
    #     # если нет столкновений возвращаем пустой список
    #     if not hit_sprites:
    #         return []
    #     # список для хранения обьектов поражанных врагов
    #     collisions_enemies = []
    #     # перебираем каждого пораженного врага
    #     for enemy_sprite in hit_sprites:
    #         # получаем обьект врага из его спрайта через функциб enemy_object которая возвращает сам обьект
    #         enemy = enemy_sprite.enemy_object
    #
    #         if not enemy.is_alive:
    #             # пропускаем мертвых врагов
    #             continue
    #
    #         # отнимаем здоровье врага, равное количеству урона в словаря текущего заклинания
    #         enemy.take_damage(self.data.get('damage'))
    #         print(f"враг {enemy.__class__.__name__} получил {self.data.get('damage')} урона")
    #         print(f"у врага {enemy.__class__.__name__} осталось еще {enemy.health.current_health} ")
    #         # добавляем врага в список пораженных
    #         collisions_enemies.append(enemy)
    #     # если заклинание не пробивающее, то оно удалится об врага, если пробивающее то вылетит насквось
    #     if not self.data.get('piercing', False):
    #         self.is_alive = False
    #     # возвращаем список обьектов пораженных врагов
    #     return collisions_enemies

    def check_and_apply_damage(self):
        """ Абстрактный класс для проверки и нансения урона, патом даделаю"""
        raise NotImplementedError("")


class SingleDamageAreaSpell(AreaSpell):
    def __init__(self, spell_id, target_x, target_y, entity_manager=None):
        super().__init__(spell_id, target_x, target_y, entity_manager)
        self.damage_frame = self.data.get('damage_frame', 5)
        self.damage_dealt = False

    def check_and_apply_damage(self):
        # если текущий кадр это кард несущий урон, и урон нужно нанести
        if (self.current_frame == self.damage_frame) and not self.damage_dealt:
            if self.entity_manager:
                # ищем врагов через метод entity_manager - get_enemies_in_hitbox
                # enemies - список врагов
                damage = self.data.get('damage', 0)
                enemies = self.entity_manager.get_enemies_in_hitbox(
                    self.target_x, self.target_y, self.hitbox_width, self.hitbox_height
                )
                for enemy in enemies:
                    enemy.take_damage(damage)
                    print(f'заклинание ебануло по {enemy.__class__.__name__}, он получил {damage} урона')
            else:
                print('нет entity_manager')


class MultiDamageAreaSpell(AreaSpell):
    def __init__(self, spell_id, target_x, target_y, entity_manager=None):
        super().__init__(spell_id, target_x, target_y, entity_manager)
        self.damage_frames = self.data.get('damage_frames', [])
        # тип нанесенного урона, сейчас я сделал только frame_damage
        self.damage_mode = self.data.get('damage_mode', 'frame_damage')
        # тоесть сейчас система урона по кадрам, а не по тикам
        # TODO сделать систему урона по тикам
        self.damage_per_hit = self.data.get('damage_per_hit', 10)

        self.processed_frames = set()  # множество уже обработанных кадров

    def check_and_apply_damage(self):
        current_frame = self.current_frame

        # если текущий кадр это кард из списка тех что несут урон, и мы еще не обработали его
        if self.current_frame in self.damage_frames and current_frame not in self.processed_frames:
            # типо уже обработали этот кадр
            self.processed_frames.add(current_frame)

            if self.entity_manager:
                # ищем врагов через метод entity_manager - get_enemies_in_hitbox
                # enemies - список врагов
                damage = self.damage_per_hit
                enemies = self.entity_manager.get_enemies_in_hitbox(
                    self.target_x, self.target_y, self.hitbox_width, self.hitbox_height
                )
                for enemy in enemies:
                    enemy.take_damage(damage)
                    print(f'заклинание ебануло по {enemy.__class__.__name__}, он получил {damage} урона')
            else:
                print('нет entity_manager')


class SunStrikeSpell(SingleDamageAreaSpell):
    def __init__(self, target_x, target_y, entity_manager):
        super().__init__('sun_strike', target_x, target_y, entity_manager)


class EarthSpikesSpell(MultiDamageAreaSpell):
    def __init__(self, target_x, target_y, entity_manager):
        super().__init__('earth_spikes', target_x, target_y, entity_manager)
