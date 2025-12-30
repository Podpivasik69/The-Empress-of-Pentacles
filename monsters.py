import arcade
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
