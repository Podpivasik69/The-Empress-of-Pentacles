import arcade


class Staff:

    def __init__(self, name, cooldown, spread_angle=0.0, damage_multiplier=1.0, sprite_path=None, grip_offset_x=25, grip_offset_y=-10):
        self.name = name
        self.cooldown = cooldown
        self.damage_multiplier = damage_multiplier
        self.sprite_path = sprite_path
        self.sprite = None
        self.spread_angle = spread_angle  # угол разброса где -1 идеальный, 0 дефолт, 1-5 разброс, >10 дробовик
        self.grip_offset_x = grip_offset_x
        self.grip_offset_y = grip_offset_y

        if sprite_path:
            self.sprite = arcade.Sprite(sprite_path)

    def get_cooldown(self):
        return self.cooldown

    def get_damage_multiplier(self):
        return self.damage_multiplier


# посохи
BASIC_STAFF = Staff(
    name="Базовый посох",
    cooldown=0.5,
    damage_multiplier=1.0,
    sprite_path="media/staffs/staff_basic2.png",
    grip_offset_x=20,
    grip_offset_y=-10,
)

FAST_STAFF = Staff(
    name="Посох скорости",
    cooldown=0.15,
    damage_multiplier=0.7,  # меньше урон за скорость
    sprite_path="media/staffs/FAST_STAFF2.png"
)

POWER_STAFF = Staff(
    name="Посох силы",
    cooldown=1.0,
    damage_multiplier=2.0,  # больше урон за медленность
    sprite_path="media/staffs/staff_power.png"
)

SNIPER_STAFF = Staff(
    name="Снайперский посох",
    cooldown=5.0,
    spread_angle=-1.0,  # идеальная точность
    damage_multiplier=4,
    sprite_path="media/staffs/staff_sniper.png"
)

# SHOTGUN_STAFF = Staff(
#     name="Дробящий посох",
#     cooldown=1.0,
#     spread_angle=15.0,  # сильный разброс
#     damage_multiplier=0.5,  # маленький урон за снаряд
#     sprite_path="media/staff_shotgun.png"
# )
