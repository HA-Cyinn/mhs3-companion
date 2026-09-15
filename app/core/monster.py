from dataclasses import dataclass
from typing import Optional

from .counters import get_counter


@dataclass(frozen=True)
class MonsterState:
    name: str
    attack_type: str

    @property
    def counter(self) -> Optional[str]:
        if self.attack_type == "unknown":
            return None
        return get_counter(self.attack_type).value


class Monster:
    """Domain model backed by the Monster JSON data."""

    def __init__(self, data: dict):
        self.name = data["name"]
        self.element = data["element"]
        self.image_url = data.get("image_url")
        self.source_url = data.get("source_url")
        self.resistances = data.get("resistances", {"ailment": {}, "element": {}})
        self.states = [
            MonsterState(s["name"], s["attack_type"])
            for s in data.get("states", [])
        ]

    def get_state(self, name: str) -> MonsterState:
        for state in self.states:
            if state.name == name:
                return state
        raise KeyError(f"Unknown state: {name}")
