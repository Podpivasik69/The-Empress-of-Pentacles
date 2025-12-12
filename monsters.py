from constants import *
import arcade
import math


# базовый класс врагов, от него будут наследоватся другие
class BaseEnemie:
    def __init__(self, health, max_health, speed, x, y, melee_damage):
        # начальные штучки
        self.health = health
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
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite_path = sprite_path
        self.sprite_scale = scale

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    def take_damage(self, amount, spell_category='fast'):


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


class TrainingTarget(BaseEnemie):
    """ПУГАЛО"""

    def __init__(self, health, max_health, speed, x, y, melee_damage):
        super().__init__(health, max_health, speed, x, y, melee_damage)

        # анимация
        self.animation_textures = []
        self.current_frame = 0
        self.animation_timer = 0.0
        self.base_animation_speed = 0.5
        self.current_speed_multiplier = 1.0
        self.hit_effect_timer = 0.0

    def setup_animation(self, base_path="media/enemies/target/target_anim/target", num_frames=17):
        # загружаем кадры
        print('загрузка мишени')
        self.animation_textures = []
        for i in range(1, num_frames + 1):
            texture_path = f"{base_path}{i}.png"
            print(f"загрузка текстур{texture_path}")
            try:
                texture = arcade.load_texture(texture_path)
                self.animation_textures.append(texture)
                print(f'текстуры {texture_path}')

            except Exception as e:
                print(f'ошибка {texture_path} - {e}')
        print(f'всего загружено {len(self.animation_textures)}')

        if self.animation_textures and self.sprite:
            self.sprite.texture = self.animation_textures[0]
        else:
            print('ошибка чет не загрузилось')

    def take_damage(self, amount, spell_category="fast"):
        result = super().take_damage(amount)
        # множитель взависимости от типа где быстрые заклиннаия 2 и тд
        multipliers = {"fast": 2.0, "medium": 3.0, "unique": 4.0}
        self.current_speed_multiplier = multipliers.get(spell_category, 10.0)
        self.hit_effect_timer = 0.5

        self.current_frame = 0  # ИЛИ self.current_frame = 8 (середина анимации для эффекта "отдачи")
        self.animation_timer = 0.0  # Сбрасываем таймер

        if self.sprite and self.animation_textures:
            self.sprite.texture = self.animation_textures[self.current_frame]
            print(
                f"🔥 ПОПАДАНИЕ! Сброс анимации. Категория: {spell_category}, Множитель: {self.current_speed_multiplier}")


        return result

    def update(self, delta_time):
        super().update(delta_time)

        if not self.is_alive or not self.animation_textures:
            return

        # Обновляем таймер эффекта
        if self.hit_effect_timer > 0:
            self.hit_effect_timer -= delta_time
            if self.hit_effect_timer <= 0:
                self.current_speed_multiplier = 1.0  # Возвращаем базовую скорость

        # Обновляем анимацию
        self.animation_timer += delta_time

        # Вычисляем скорость с учетом множителя
        frame_duration = self.base_animation_speed / self.current_speed_multiplier

        if self.animation_timer >= frame_duration:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_textures)

            if self.sprite:
                self.sprite.texture = self.animation_textures[self.current_frame]


