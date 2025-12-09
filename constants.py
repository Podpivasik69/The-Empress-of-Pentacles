SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"

# константы
# категории снарядов (быстрые/средние/тяжелые)
PROJECTILE_CATEGORIES = {
    "fast": {  # искры, всплески
        "speed": 800,
        "damage": 10,
        "size": 16
    },
    "medium": {  # шары, стандартные
        "speed": 500,
        "damage": 30,
        "size": 32
    },
    "slow": {  # тяжелые
        "speed": 300,
        "damage": 50,
        "size": 48
    }
}
# уникальные спелы
PROJECTILE_EXCEPTIONS = {
    "sun_strike": {  # УНИКАЛЬНЫЙ
        "speed": 350,  # не совсем slow
        "damage": 70,  # больше чем slow
        "size": 40,
        "homing": True,  # преследует цель
        "effect": "burning"
    },
    "water_cannon": {  # УНИКАЛЬНЫЙ
        "speed": 600,  # между fast и medium
        "damage": 25,
        "size": 24,
        "piercing": True,  # проходит сквозь врагов
        "effect": "slow"
    }
}
# мапинг
SPELL_TO_CATEGORY = {
    "fire_spark": "fast",
    "splashing_water": "fast",
    "fireball": "medium",
    "waterball": "medium",
}
# пути до спрайтов
SPELL_ICONS = {
    # огонь
    "fire_spark": ("media/spels/fire_spark _icon.png"),
    "fireball": ("media/spels/fireball_icon.png"),
    "sun_strike": ('media/spels/sun_strike_icon.png'),
    # вода
    "splashing_water": ("media/spels/splashing_water_icon.png"),
    "waterball": ("media/spels/waterball_icon.png"),
    "water_cannon": ("media/spels/water_cannon_icon.png"),
    # земля (позже)
    "earth_pebble": "media/placeholder_icon.png",
    "stone_spike": "media/placeholder_icon.png",
    "earthquake": "media/placeholder_icon.png",

    # воздух (позже)
    "wind_gust": "media/placeholder_icon.png",
    "tornado": "media/placeholder_icon.png",
    "lightning_bolt": "media/placeholder_icon.png",
}

# словрь для времени перезарядки заклинаний
SPELL_RELOAD_TIMES = {
    "fire_spark": 0.5,
    "fireball": 2.0,
    "sun_strike": 5.0,

    "splashing_water": 0.35,
    "waterball": 2.0,
    "water_cannon": 4.0,
}
