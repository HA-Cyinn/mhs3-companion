from pathlib import Path
import json

from .monster import Monster

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "monsters.json"


def load_monsters() -> list[Monster]:
    with DATA_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Monster(data) for data in raw["monsters"]]
