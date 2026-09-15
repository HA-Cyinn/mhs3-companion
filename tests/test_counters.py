
from app.core.counters import AttackType, get_counter


def test_power_counter():
    assert get_counter("power") == AttackType.SPEED


def test_speed_counter():
    assert get_counter("speed") == AttackType.TECHNICAL


def test_technical_counter():
    assert get_counter("technical") == AttackType.POWER
