import arcade
from physics import *
import math
from core.components.health import Health


# базовый класс врагов, от него будут наследоватся другие
class BaseEnemie:
    def __init__(self, health, max_health, speed, x, y, melee_damage):
        # начальные штучки
        self.health = Health(max_health, health)
        self.max_health = max_health
        self.speed = speed
        self.x = x
        self.y = y
        self.melee_damage = melee_damage
        self.is_alive = True

        # спрайты
        self.sprite = None
        self.sprite_path = None
        self.sprite_scale = 1.0

    def setup(self):
        pass

    def setup_sprite(self, sprite_path, scale, sprite_list=None):
        if sprite_path:
            self.sprite = arcade.Sprite(sprite_path, scale=scale)
        else:
            self.sprite = arcade.Sprite('media/enemies/error.png', scale=scale)

        self.sprite.enemy_object = self  # важная строчка с атрибутом имени которое равно обекту
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite_path = sprite_path
        self.sprite_scale = scale

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    def take_damage(self, amount):
        """Метод для получения урон врагом True - враг умер False -  dhfu lbdjq"""

        print(f"[DEBUG] BaseEnemie.take_damage вызван с amount={amount}")
        print(f"[DEBUG] self.is_alive = {self.is_alive}")

        if not self.is_alive:
            print(f"[DEBUG] Враг уже мертв, возвращаем True")

            print(f"{BaseEnemie} враг уде мертв")
            return False

        print(f"[DEBUG] Вызываем self.health.take_damage({amount})")

        # take_damage - False = выжил
        dead = self.health.take_damage(amount)
        print(f"[DEBUG] self.health.take_damage вернул: {dead}")
        print(dead)
        if dead:
            print(f"[DEBUG] Враг должен умереть!")
            self.die()
            return True  # враг здох

        print(f"[DEBUG] Враг выжил")
        return False  # выжил сволоч

    def die(self):
        # смерть!
        self.is_alive = False
        print('он умер')
        if self.sprite:
            self.sprite.remove_from_sprite_lists()
            self.sprite = None

    def draw(self):
        """Для отладки или особых случаев"""
        if self.sprite and self.is_alive:
            self.sprite.draw()

    def update(self, delta_time):
        """Базовый update. Для мишени - ничего не делает"""
        if not self.is_alive:
            return


class TestEnemie(BaseEnemie):
    def __init__(self, health, max_health, speed, x, y, melee_damage=0):
        super().__init__(health, max_health, speed, x, y, melee_damage)

    def take_damage(self, amount):
        return super().take_damage(amount)

    def update(self, delta_time):
        pass

    def die(self):
        super().die()

    def update_sprite_position(self, camera_x, camera_y, cell_size):
        if self.sprite:
            enemy_pixel_x = self.x * cell_size - camera_x
            enemy_pixel_y = self.y * cell_size - camera_y
            self.sprite.center_x = enemy_pixel_x
            self.sprite.center_y = enemy_pixel_y


class BarrelEnemy(BaseEnemie):
    def __init__(self, x, y, substance_type=None):
        if substance_type is None:
            substance_type = random.choice(
                ['water', 'lava', 'acid', 'powder', 'plasm',
                 'petrol', 'fire', 'snow'])
        self.substance_type = substance_type

        super().__init__(
            health=1,
            max_health=1,
            speed=0,
            x=x,
            y=y,
            melee_damage=0
        )

        self.explosion_radius = 10
        self.sprite_path = 'media/enemies/barrel.png'
        self.hit_radius = 8
        self.exploded = False
        self.sub_n = 100

    def setup_sprite(self, sprite_path=None, scale=0.2, sprite_list=None):
        if sprite_path is None:
            sprite_path = self.sprite_path
        super().setup_sprite(sprite_path, scale, sprite_list)

    def check_collision(self, projectile_x, projectile_y, projectile_radius=0):
        distance = math.sqrt(
            (projectile_x - self.x) ** 2 +
            (projectile_y - self.y) ** 2
        )
        return distance <= self.hit_radius

    def take_damage(self, amount, projectile_x=None, projectile_y=None):
        if projectile_x is not None and projectile_y is not None:
            if not self.check_collision(projectile_x, projectile_y):
                return False

        dead = super().take_damage(amount)

        if dead and not self.exploded:
            self.explode()
            return True

        return dead

    def explode(self):
        if self.exploded:
            return

        self.exploded = True

        created_count = 0

        for _ in range(self.sub_n):
            dx = random.randint(-self.explosion_radius, self.explosion_radius)
            dy = random.randint(-self.explosion_radius, self.explosion_radius)

            new_x = int(self.x + dx)
            new_y = int(self.y + dy)

            try:
                if self.substance_type == 'lava':
                    substance = Lava(new_x, new_y, stone)
                elif self.substance_type == 'water':
                    substance = Water(new_x, new_y)
                elif self.substance_type == 'acid':
                    substance = Acid(new_x, new_y)
                elif self.substance_type == 'powder':
                    substance = Powder(new_x, new_y)
                elif self.substance_type == 'stone':
                    substance = Stone(new_x, new_y)
                elif self.substance_type == 'sand':
                    substance = Sand(new_x, new_y)
                elif self.substance_type == 'wood':
                    substance = Wood(new_x, new_y)
                elif self.substance_type == 'iron':
                    substance = Iron(new_x, new_y)
                elif self.substance_type == 'smoke':
                    substance = Smoke(new_x, new_y)
                elif self.substance_type == 'steam':
                    substance = Steam(new_x, new_y)
                elif self.substance_type == 'plasm':
                    substance = Plasm(new_x, new_y)
                elif self.substance_type == 'petrol':
                    substance = Petrol(new_x, new_y)
                elif self.substance_type == 'boom':
                    substance = Boom(new_x, new_y)
                elif self.substance_type == 'fire':
                    substance = Fire(new_x, new_y)
                elif self.substance_type == 'snow':
                    substance = Snow(new_x, new_y)
                elif self.substance_type == 'ground':
                    substance = Ground(new_x, new_y)
                elif self.substance_type == 'grass':
                    substance = Grass(new_x, new_y)
                else:
                    continue

                add_substance(substance)
                created_count += 1
            except:
                pass

        try:
            center_x, center_y = int(self.x), int(self.y)
            if self.substance_type == 'lava':
                substance = Lava(center_x, center_y, stone)
            elif self.substance_type == 'water':
                substance = Water(center_x, center_y)
            elif self.substance_type == 'acid':
                substance = Acid(center_x, center_y)
            elif self.substance_type == 'powder':
                substance = Powder(center_x, center_y)
            elif self.substance_type == 'stone':
                substance = Stone(center_x, center_y)
            elif self.substance_type == 'sand':
                substance = Sand(center_x, center_y)
            elif self.substance_type == 'wood':
                substance = Wood(center_x, center_y)
            elif self.substance_type == 'iron':
                substance = Iron(center_x, center_y)
            elif self.substance_type == 'smoke':
                substance = Smoke(center_x, center_y)
            elif self.substance_type == 'steam':
                substance = Steam(center_x, center_y)
            elif self.substance_type == 'plasm':
                substance = Plasm(center_x, center_y)
            elif self.substance_type == 'petrol':
                substance = Petrol(center_x, center_y)
            elif self.substance_type == 'boom':
                substance = Boom(center_x, center_y)
            elif self.substance_type == 'fire':
                substance = Fire(center_x, center_y)
            elif self.substance_type == 'snow':
                substance = Snow(center_x, center_y)
            elif self.substance_type == 'ground':
                substance = Ground(center_x, center_y)
            elif self.substance_type == 'grass':
                substance = Grass(center_x, center_y)

            add_substance(substance)
            created_count += 1
        except:
            pass

        self.die()

    def die(self):
        self.is_alive = False
        if self.sprite:
            self.sprite.remove_from_sprite_lists()
            self.sprite = None

    def update(self, delta_time):
        pass

    def is_explosive(self):
        return self.substance_type in ['water', 'lava', 'powder', 'petrol', 'boom', 'plasm', 'fire']

    @classmethod
    def create_random(cls, x, y):
        substance_types = ['water', 'lava', 'acid', 'powder', 'stone', 'sand', 'wood', 'iron', 'smoke', 'steam',
                           'plasm', 'petrol', 'boom', 'fire', 'snow', 'ground', 'grass']
        return cls(x, y, random.choice(substance_types))


class GhostEnemy(BaseEnemie):
    def __init__(self, health, max_health, speed, x, y, melee_damage=0):
        super().__init__(health, max_health, speed, x, y, melee_damage)
        self.speed = speed
        self.is_ghost = True

    def update(self, delta_time):
        pass

    def setup_sprite(self, sprite_path, scale, sprite_list=None):
        if sprite_path:
            self.sprite = arcade.Sprite(sprite_path, scale=scale)
        else:
            self.sprite = arcade.Sprite('media/enemies/error.png', scale=scale)

        self.sprite.enemy_object = self
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite_path = sprite_path
        self.sprite_scale = scale

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    def die(self):
        self.is_alive = False
        print('Призрак умер')
        if self.sprite:
            self.sprite.remove_from_sprite_lists()
            self.sprite = None
        # Получаем доступ к игроку через game_view
        if hasattr(self, 'game_view'):
            self.game_view.player.kill_num += 1