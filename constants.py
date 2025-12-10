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
# балистика
TRAJECTORY_CONFIG = {
    "fast": {
        "gravity": 0,  # Без гравитации
        "arc_height": 0,  # Без дуги
        "lifetime": 2.0,  # Время жизни
        "max_distance": 600  # Макс дистанция
    },
    "medium": {
        "gravity": 400,  # Сила гравитации
        "arc_height": 100,  # Высота дуги
        "lifetime": 3.0,
        "max_distance": 400
    },
    "unique": {
        "gravity": 0,
        "arc_height": 0,
        "lifetime": 4.0,
        "max_distance": 800
    }
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
        "size": 32,
    },

    "fireball": {
        "category": "medium",
        "icon": "media/spells/fireball_icon.png",
        "reload_time": 2.0,
        "speed": 500,
        "damage": 30,
        "size": 32,
        "rotates": True,
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
        "size": 32,
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
