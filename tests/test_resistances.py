import json
from pathlib import Path

from app.core.data import load_monsters


def test_all_monsters_have_two_resistance_groups():
    monsters = load_monsters()
    assert len(monsters) == 131

    for monster in monsters:
        assert set(monster.resistances) == {"ailment", "element"}
        assert set(monster.resistances["ailment"]) == {
            "poison", "burn", "paralysis", "sleep", "blastblight", "bleeding", "darkness"
        }
        assert set(monster.resistances["element"]) == {
            "neutral", "fire", "water", "thunder", "ice", "dragon"
        }


def test_pukei_pukei_resistances_are_imported():
    monster = next(m for m in load_monsters() if m.name == "Pukei-Pukei")
    assert monster.resistances["element"]["water"] == "very_resistant"
    assert monster.resistances["element"]["thunder"] == "sensitive"
    assert monster.resistances["element"]["dragon"] == "very_sensitive"


def test_unknown_source_value_is_not_guessed():
    monster = next(m for m in load_monsters() if m.name == "Great Poogie")
    assert all(value == "unknown" for value in monster.resistances["ailment"].values())
