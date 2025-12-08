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