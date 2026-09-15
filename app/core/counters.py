
from enum import Enum


class AttackType(str, Enum):
    POWER = "power"
    TECHNICAL = "technical"
    SPEED = "speed"


COUNTERS = {
    AttackType.POWER: AttackType.SPEED,
    AttackType.SPEED: AttackType.TECHNICAL,
    AttackType.TECHNICAL: AttackType.POWER,
}


def get_counter(attack_type: str) -> AttackType:
    """Return the attack type that counters the monster's attack type."""
    try:
        attack = AttackType(attack_type.lower())
    except ValueError as exc:
        raise ValueError(f"Unknown attack type: {attack_type}") from exc
    return COUNTERS[attack]
