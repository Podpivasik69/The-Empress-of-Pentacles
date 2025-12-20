from projectile import SunStrikeProjectile, Projectile
from monsters import TrainingTarget
from constants import *
import random
import arcade
import math


class ProjectileManager:
    def __init__(self, game_state, entity_manager):
        self.game_state = game_state
        self.entity_manager = entity_manager
        self.projectiles = []

    def update(self, delta_time):

        if self.game_state.want_to_shoot and self.game_state.can_shoot:
            self.create_shoot()
            self.game_state.want_to_shoot = False
        # стреляем спелами
        for projectile in self.projectiles:
            projectile.update(delta_time)

        self.check_collisions()
        # удаляем старье
        self.projectiles = [p for p in self.projectiles if p.is_alive]

    def create_projectile(self, spell_type, start_x, start_y, target_x, target_y, spread_angle=0.0, launch_angle=None):
        """ Создание снаряда по готовым параметрам """

        if self.game_state.active_spell == "sun_strike":
            # Санстрайк
            projectile = SunStrikeProjectile(
                center_x=target_x,  # X курсора
                center_y=SCREEN_HEIGHT // 2,  # 300px (центр экрана)
                damage=SPELL_DATA["sun_strike"]["damage"]
            )
        else:
            # Обычные снаряды
            projectile = Projectile(
                spell_type=spell_type,
                start_x=start_x,
                start_y=start_y,
                target_x=target_x,
                target_y=target_y,
                spread_angle=spread_angle,
                launch_angle=launch_angle,
            )
        self.projectiles.append(projectile)
        return projectile

    def create_shoot(self):
        """ Вычисление всех параметров и создание снаряда """

        staff_sprite = self.entity_manager.staff_sprite
        spread = self.game_state.current_staff.spread_angle  # угол разброса

        if staff_sprite:
            # вычисление угла в радианах
            arcade_angle = staff_sprite.angle
            math_angle = math.radians(90 - staff_sprite.angle)

            # примерно 3/4 от высоты
            staff_length = staff_sprite.height * 0.5

            # точка на конце посоха
            start_x = staff_sprite.center_x + math.cos(math_angle) * staff_length
            start_y = staff_sprite.center_y + math.sin(math_angle) * staff_length

            # ПРИМЕНЯЕМ SPREAD К УГЛУ
            if spread > 0:
                spread_rad = math.radians(spread)
                math_angle += random.uniform(-spread_rad, spread_rad)
                print(f"  Spread применен: {spread}°")
                print(f"  Новый угол после spread: {math.degrees(math_angle):.1f}°")

            launch_angle = math_angle
            # точка вылета
            print(f"выстрел : ({start_x:.0f}, {start_y:.0f}), угол: {staff_sprite.angle:.0f}°")
        else:
            start_x = self.game_state.player.center_x
            start_y = self.game_state.player.center_y
            launch_angle = None

        projectile = self.create_projectile(
            spell_type=self.game_state.active_spell,
            start_x=start_x,
            start_y=start_y,
            target_x=self.game_state.shoot_target_x,
            target_y=self.game_state.shoot_target_y,
            spread_angle=spread,
            launch_angle=launch_angle
        )
        # типо после выстрела ты не можещь стрелять и идет кд
        self.game_state.can_shoot = False  # задержка посоха
        self.game_state.shoot_timer = self.game_state.shoot_cooldown

        reload_time = SPELL_DATA.get(self.game_state.active_spell, {}).get("reload_time", 3.0)

        print(f'Задержка посоха! Осталось: {self.game_state.shoot_timer:.1f}с')

    def draw(self):
        for projectile in self.projectiles:
            projectile.draw()

    def check_collisions(self):
        # списки врагов и снарядов для удаления
        enemies_to_remove = []
        projectiles_to_remove = []

        # ПЕРВЫЙ ПРОХОД: собираем что нужно удалить
        for projectile in self.projectiles:
            if not projectile.is_alive:
                continue

            # перебираем всех врагов
            for enemy in self.game_state.enemies:
                # Пропускаем мертвых врагов или без спрайта
                if not enemy.is_alive or not enemy.sprite:
                    continue

                # Проверяем столкновение
                if arcade.check_for_collision(projectile.sprite, enemy.sprite):
                    print(f"Попадание! Снаряд {projectile.spell_type} попал во врага")

                    # Наносим урон врагу
                    damage_amount = 10  # TODO: брать из данных заклинания
                    if isinstance(enemy, TrainingTarget):
                        spell_category = SPELL_DATA.get(projectile.spell_type, {}).get("category", "fast")
                        enemy_died = enemy.take_damage(damage_amount, spell_category)
                    else:
                        enemy_died = enemy.take_damage(damage_amount)

                    # Помечаем снаряд для удаления
                    projectiles_to_remove.append(projectile)

                    # Если враг умер - добавляем в список на удаление
                    if enemy_died:
                        print("Враг уничтожен!")
                        enemies_to_remove.append(enemy)
                        # Удаляем спрайт врага из списка отрисовки

                    break  # Снаряд попал - выходим из цикла по врагам

        # ВТОРОЙ ПРОХОД: удаляем собранные объекты
        for enemy in enemies_to_remove:
            if enemy in self.game_state.enemies:
                self.game_state.enemies.remove(enemy)
                if enemy.sprite and enemy.sprite in self.entity_manager.enemy_sprites:
                    self.entity_manager.enemy_sprites.remove(enemy.sprite)

        for projectile in projectiles_to_remove:
            projectile.is_alive = False
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)
