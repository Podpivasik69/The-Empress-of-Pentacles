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
        "category": "fast",
        "icon": "media/spells/fire_spark_icon.png",
        "reload_time": 0.5,
        "speed": 800,
        "damage": 10,
        "size": 16,
    },

    "fireball": {
        "category": "medium",
        "icon": "media/spells/fireball_icon.png",
        "reload_time": 2.0,
        "speed": 500,
        "damage": 30,
        "size": 32,
    },

    "sun_strike": {
        "category": "unique",
        "icon": "media/spells/sun_strike_icon.png",
        "reload_time": 5.0,
        "speed": 350,
        "damage": 70,
        "size": 40,
        "homing": True,
        "effect": "burning",
    },

    # вода
    "splashing_water": {
        "category": "fast",
        "icon": "media/spells/splashing_water_icon.png",
        "reload_time": 0.35,
        "speed": 800,
        "damage": 10,
        "size": 16,
    },

    "waterball": {
        "category": "medium",
        "icon": "media/spells/waterball_icon.png",
        "reload_time": 2.0,
        "speed": 500,
        "damage": 30,
        "size": 32,
    },

    "water_cannon": {
        "category": "unique",
        "icon": "media/spells/water_cannon_icon.png",
        "reload_time": 4.0,
        "speed": 600,
        "damage": 25,
        "size": 24,
        "piercing": True,
        "effect": "slow",
    },
}

# категории снарядов (быстрые/средние/тяжелые)
# PROJECTILE_CATEGORIES = {
#     "fast": {  # искры, всплески
#         "speed": 800,
#         "damage": 10,
#         "size": 16
#     },
#     "medium": {  # шары, стандартные
#         "speed": 500,
#         "damage": 30,
#         "size": 32
#     },
#     "slow": {  # тяжелые
#         "speed": 300,
#         "damage": 50,
#         "size": 48
#     }
# }
# уникальные спелы
# PROJECTILE_EXCEPTIONS = {
#     "sun_strike": {  # УНИКАЛЬНЫЙ
#         "speed": 350,  # не совсем slow
#         "damage": 70,  # больше чем slow
#         "size": 40,
#         "homing": True,  # преследует цель
#         "effect": "burning"
#     },
#     "water_cannon": {  # УНИКАЛЬНЫЙ
#         "speed": 600,  # между fast и medium
#         "damage": 25,
#         "size": 24,
#         "piercing": True,  # проходит сквозь врагов
#         "effect": "slow"
#     }
# }
# мапинг
# SPELL_TO_CATEGORY = {
#     "fire_spark": "fast",
#     "splashing_water": "fast",
#     "fireball": "medium",
#     "waterball": "medium",
# }
# пути до спрайтов
# SPELL_ICONS = {
#     # огонь
#     "fire_spark": ("media/spells/fire_spark _icon.png"),
#     "fireball": ("media/spells/fireball_icon.png"),
#     "sun_strike": ('media/spells/sun_strike_icon.png'),
#     # вода
#     "splashing_water": ("media/spells/splashing_water_icon.png"),
#     "waterball": ("media/spells/waterball_icon.png"),
#     "water_cannon": ("media/spells/water_cannon_icon.png"),
#     # земля (позже)
#     "earth_pebble": "media/placeholder_icon.png",
#     "stone_spike": "media/placeholder_icon.png",
#     "earthquake": "media/placeholder_icon.png",
#
#     # воздух (позже)
#     "wind_gust": "media/placeholder_icon.png",
#     "tornado": "media/placeholder_icon.png",
#     "lightning_bolt": "media/placeholder_icon.png",
# }

# словрь для времени перезарядки заклинаний
# SPELL_RELOAD_TIMES = {
#     "fire_spark": 0.5,
#     "fireball": 2.0,
#     "sun_strike": 5.0,
#
#     "splashing_water": 0.35,
#     "waterball": 2.0,
#     "water_cannon": 4.0,
# }
