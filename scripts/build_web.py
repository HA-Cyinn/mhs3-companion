"""Generate the PWA assets (web/data.json, web/img/*.webp, web/precache.json) from app/data."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DATA = ROOT / "app" / "data" / "monsters.json"
SRC_IMAGES = ROOT / "app" / "data" / "images"
WEB = ROOT / "web"
OUT_IMAGES = WEB / "img"

AILMENTS = ["poison", "burn", "paralysis", "sleep", "blastblight", "bleeding", "darkness"]
ELEMENTS = ["neutral", "fire", "water", "thunder", "ice", "dragon"]
ATTACK_CODES = {"power": "p", "speed": "s", "technical": "t", "unknown": "?"}
LEVEL_CODES = {
    "very_sensitive": 0, "sensitive": 1, "normal": 2,
    "resistant": 3, "very_resistant": 4, "unknown": 5,
}


def safe_name(key: str) -> str:
    # Match the sanitized filenames used by the source image cache.
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in key).strip("_") or "image"


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> None:
    raw = json.loads(SRC_DATA.read_text(encoding="utf-8"))["monsters"]

    if OUT_IMAGES.exists():
        shutil.rmtree(OUT_IMAGES)
    OUT_IMAGES.mkdir(parents=True)

    monsters = []
    images = 0
    for m in raw:
        key = slug(m["name"])
        entry = {
            "id": key,
            "n": m["name"],
            "e": m["element"],
            "s": [[s["name"], ATTACK_CODES[s["attack_type"]]] for s in m.get("states", [])],
            "a": [LEVEL_CODES[m["resistances"]["ailment"][k]] for k in AILMENTS],
            "r": [LEVEL_CODES[m["resistances"]["element"][k]] for k in ELEMENTS],
        }
        src = SRC_IMAGES / f"{safe_name(m['name'])}.png"
        if src.exists():
            Image.open(src).convert("RGBA").save(OUT_IMAGES / f"{key}.webp", "WEBP", quality=80, method=6)
            entry["i"] = 1
            images += 1
        monsters.append(entry)

    (WEB / "data.json").write_text(
        json.dumps(monsters, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    files = sorted(
        ["./", "index.html", "style.css", "app.js", "data.json", "manifest.webmanifest",
         "icon-192.png", "icon-512.png"]
        + [f"img/{p.name}" for p in OUT_IMAGES.glob("*.webp")]
    )
    (WEB / "precache.json").write_text(json.dumps(files), encoding="utf-8")
    print(f"{len(monsters)} monstres, {images} images, {len(files)} fichiers à précacher")


if __name__ == "__main__":
    main()
