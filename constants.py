SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"

# константы

ELEMENTS = {
    "fire": "↑",
    "water": "←",
    "earth": "↓",
    "air": "→"
}

UI_SETTINGS = {
    "quickbar_slots": 4,
    "quickbar_slot_size": 64,
    "inventory_rows": 5,
    "inventory_cols": 8,
    "health_bar_width": 200,
    "health_bar_height": 20,
}

PLAYER_SETTINGS = {
    "speed": 300,
    "health": 100,
    "invulnerability_time": 1.0,
}

# нихуя себе - новый словарь
SPELL_DATA = {
    # огонь
    "fire_spark": {
        "spell_type": "linear_projectile",
        'elemental_type': "fire",

        "icon": "media/ui/spells_icons/fire_spark_icon.png",
        "game_sprite": 'media/spells/fire_spark.png',

        "reload_time": 0.5,
        "speed": 800,
        "gravity": 0,
        "damage": 30,
        "size": 32,
        "mana_cost": 5,
    },

    "fireball": {
        "spell_type": "parabolic_projectile",
        'elemental_type': "fire",

        "icon": "media/ui/spells_icons/fireball_icon.png",
        "game_sprite": 'media/spells/fireball.png',

        "reload_time": 2.0,
        "speed": 500,
        "gravity": 500,
        "gravity_exponent": 1,
        "damage": 30,
        "size": 32,
        "rotates": True,
        "mana_cost": 15,
    },

    "sun_strike": {
        # ОДА ДЕТКА Я ПОВЕЛИТЕЛЬ САНСТРАЙКОВ
        "spell_type": "area_spell",
        "damage_type": "single",  # одиночный сильный урон на нужном кадре
        "damage_frame": 5,  # кадр на котором будет урон
        "elemental_type": "fire",

        "icon": "media/ui/spells_icons/sun_strike_icon.png",
        "reload_time": 4.0,

        # анимация
        "total_frames": 12,  # всего кадров
        "frame_duration": 0.1,  # задержка, 100 мс на каждый кадр, всего типо 1.2 секунды на весь цикл

        # боевые параметры
        "damage": 500,
        # ширина, высота спрайта
        "base_width": 172,
        "base_height": 442,
        "sprite_scale": 0.7,

        "delay_to_cast": 0.3,  # задержка перед началом анимации
        "piercing": True,  # ЕСТЬ ПРОБИТИЕ

        "frame_path": "media/spells/new_sun_strike/spr_meteor_shower_{}.png",

        "mana_cost": 50,
    },

    # вода
    "splashing_water": {
        "spell_type": "linear_projectile",
        "elemental_type": "water",

        "icon": "media/ui/spells_icons/splashing_water_icon.png",
        "game_sprite": 'media/spells/splashing_water.png',

        "reload_time": 0.35,
        "speed": 800,
        "gravity": 0,
        "damage": 10,
        "size": 32,
        "mana_cost": 5,
    },

    "waterball": {
        "spell_type": "parabolic_projectile",
        "elemental_type": "water",

        "icon": "media/ui/spells_icons/waterball_icon.png",
        "game_sprite": 'media/spells/waterball.png',

        "reload_time": 2.0,
        "speed": 500,
        "gravity": 400,
        "gravity_exponent": 1.3,
        "damage": 30,
        "size": 32,
        "mana_cost": 15,
    },

    "water_cannon": {
        "spell_type": "linear_projectile",
        "elemental_type": "water",

        "icon": "media/ui/spells_icons/water_cannon_icon.png",
        "game_sprite": 'media/spells/water_cannon.png',

        "reload_time": 4.0,
        "speed": 600,
        "gravity": 0,
        "damage": 25,
        "size": 24,
        "mana_cost": 25,
        "piercing": True,
        "effect": "slow",
    },
    # земля
    # "stone_throw": {
    #     "spell_type": "linear_projectile",
    #     "elemental_type": "water",
    #
    #     "icon": "media/ui/spells_icons/splashing_water_icon.png",
    #     "game_sprite": 'media/spells/splashing_water.png',
    #
    #     "reload_time": 0.35,
    #     "speed": 800,
    #     "gravity": 0,
    #     "damage": 10,
    #     "size": 32,
    #     "mana_cost": 5,
    # },

    "earth_spikes": {
        "spell_type": "area_spell",
        "elemental_type": "earth",
        "damage_type": "multi",
        "damage_mode": "frame_damage",  # или tick_damage
        "damage_frames": [4, 5, 6, 7, 8, 9],  # карды несущие урон
        "damage_per_hit": 20,  # урон за каждый удар

        "icon": "media/ui/spells_icons/earth_spikes.png",
        "reload_time": 4.0,

        # анимация
        "total_frames": 10,  # всего кадров
        "frame_duration": 0.09,  # задержка, 90 мс на каждый кадр, всего типо 0.9 секунды на весь цикл

        # ширина, высота спрайта
        "base_width": 314,
        "base_height": 102,
        "sprite_scale": 1,

        "delay_to_cast": 0.3,  # задержка перед началом анимации
        "piercing": True,  # ЕСТЬ ПРОБИТИЕ

        "frame_path": "media/spells/earth_spikes/spr_earth_spike_{}.png",

        "mana_cost": 50,
    },

    # "water_cannon": {
    #     "spell_type": "linear_projectile",
    #     "elemental_type": "water",
    #
    #     "icon": "media/ui/spells_icons/water_cannon_icon.png",
    #     "game_sprite": 'media/spells/water_cannon.png',
    #
    #     "reload_time": 4.0,
    #     "speed": 600,
    #     "gravity": 0,
    #     "damage": 25,
    #     "size": 24,
    #     "mana_cost": 25,
    #     "piercing": True,
    #     "effect": "slow",
    # },
}
