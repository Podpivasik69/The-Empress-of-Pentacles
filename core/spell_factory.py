from core.spells_models import (
    LinearProjectileSpell, FireSparkSpell, WaterSplashingSpell,
    ParabolicProjectileSpell, FireBallSpell, WaterBallSpell,
    AreaSpell, SunStrikeSpell
)
from constants import *


def create_spell(spell_id, start_x, start_y, target_x, target_y, entity_manager=None):
    # словарь со всеми данными от нужного нам заклинания
    spell_data = SPELL_DATA[spell_id]
    spell_type = spell_data.get('spell_type')
    if spell_id == "fire_spark":
        return FireSparkSpell(start_x, start_y, target_x, target_y)
    elif spell_id == "splashing_water":
        return WaterSplashingSpell(start_x, start_y, target_x, target_y)
    #
    elif spell_id == "fireball":
        return FireBallSpell(start_x, start_y, target_x, target_y)
    elif spell_id == "waterball":
        return WaterBallSpell(start_x, start_y, target_x, target_y)

    elif spell_id == "sun_strike":
        return SunStrikeSpell(target_x, target_y, entity_manager)
