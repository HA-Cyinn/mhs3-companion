"""Import Game8 resistance cells from the supplied Markdown scrape into monsters.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/mnt/data/mhs3_source/Fichier markdown(1).md collé")
DATA_FILE = ROOT / "app" / "data" / "monsters.json"

AILMENTS = [
    "poison", "burn", "paralysis", "sleep", "blastblight", "bleeding", "darkness"
]
ELEMENTS = [
    "neutral", "fire", "water", "thunder", "ice", "dragon"
]

# Game8 uses image cells for the five resistance levels.
# The special 4441129 image is a placeholder in the supplied scrape (used
# where Game8 has not supplied a concrete resistance value).
IMAGE_TO_LEVEL = {
    "4428836": "very_sensitive",  # ↓↓
    "4428839": "sensitive",       # ↓
    "4428850": "normal",          # —
    "4428841": "resistant",       # ↑
    "4428845": "very_resistant",  # ↑↑
    "4441129": "unknown",         # placeholder / value not specified
}

MONSTER_RE = re.compile(
    r"\[\*\*([^*]+)\*\*\]\((https://game8\.co/[^)]+)\) "
    r"\(\[image\]\((https://img\.game8\.co/[^)]+)\)\)"
)
IMAGE_RE = re.compile(r"https://img\.game8\.co/(\d+)/[^)]+\.png/show")


def clean_name(raw: str) -> str:
    # The scrape duplicates many monster names inside the bold link text:
    # AjarakanAjarakan, Feral AjarakanFeral Ajarakan, etc.
    if len(raw) % 2 == 0 and raw[: len(raw) // 2] == raw[len(raw) // 2 :]:
        return raw[: len(raw) // 2]
    return raw


def extract() -> dict[str, list[str]]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    result: dict[str, list[str]] = {}
    current_name: str | None = None

    for line in lines:
        monster_match = MONSTER_RE.search(line)
        if monster_match:
            current_name = clean_name(monster_match.group(1))
            # Some monsters have no separate resistance row: Game8 places
            # the 13 resistance image cells directly on the monster row.
            ids = IMAGE_RE.findall(line)
            if len(ids) >= 14:
                result[current_name] = ids[-13:]
            continue

        if current_name is None or not line.startswith("|"):
            continue

        # Resistance rows are the only table rows containing exactly 13
        # [text](image) cells: 7 ailments + 6 elements.
        if "[text]" not in line:
            continue
        ids = IMAGE_RE.findall(line)
        if len(ids) != 13:
            continue

        if current_name not in result:
            result[current_name] = ids

    return result


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    monsters = data["monsters"]
    extracted = extract()

    missing_monsters: list[str] = []
    unknown_cells = 0
    imported = 0

    for monster in monsters:
        name = monster["name"]
        ids = extracted.get(name)
        if ids is None:
            missing_monsters.append(name)
            levels = ["unknown"] * 13
        else:
            levels = []
            for image_id in ids:
                level = IMAGE_TO_LEVEL.get(image_id, "unknown")
                if level == "unknown":
                    unknown_cells += 1
                levels.append(level)
            imported += 1

        monster["resistances"] = {
            "ailment": dict(zip(AILMENTS, levels[:7])),
            "element": dict(zip(ELEMENTS, levels[7:])),
        }

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Monstres JSON : {len(monsters)}")
    print(f"Résistances extraites : {imported}")
    print(f"Monstres sans ligne de résistance : {len(missing_monsters)}")
    if missing_monsters:
        print("  " + ", ".join(missing_monsters))
    print(f"Cellules inconnues/placeholder : {unknown_cells}")
    print(f"Lignes source reconnues : {len(extracted)}")


if __name__ == "__main__":
    main()
