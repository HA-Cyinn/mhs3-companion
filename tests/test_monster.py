from app.core.monster import Monster


def test_monster_computes_counter_from_attack_type():
    monster = Monster({
        "name": "Test",
        "element": "Fire",
        "states": [{"name": "Normal", "attack_type": "technical"}],
    })
    assert monster.get_state("Normal").counter == "power"


def test_unknown_attack_has_no_counter():
    monster = Monster({
        "name": "Test",
        "element": "Unknown",
        "states": [{"name": "Exposed", "attack_type": "unknown"}],
    })
    assert monster.get_state("Exposed").counter is None
