import json
from pathlib import Path

from scripts import build_web


ROOT = Path(__file__).resolve().parents[1]


def test_generated_web_data_matches_checked_in_assets(tmp_path, monkeypatch):
    generated_web = tmp_path / "web"
    monkeypatch.setattr(build_web, "WEB", generated_web)
    monkeypatch.setattr(build_web, "OUT_IMAGES", generated_web / "img")

    build_web.main()

    checked_in_web = ROOT / "web"
    generated_data = json.loads((generated_web / "data.json").read_text(encoding="utf-8"))
    checked_in_data = json.loads((checked_in_web / "data.json").read_text(encoding="utf-8"))
    generated_precache = json.loads((generated_web / "precache.json").read_text(encoding="utf-8"))
    checked_in_precache = json.loads((checked_in_web / "precache.json").read_text(encoding="utf-8"))

    assert generated_data == checked_in_data
    assert generated_precache == checked_in_precache
    assert {path.name for path in (generated_web / "img").glob("*.webp")} == {
        path.name for path in (checked_in_web / "img").glob("*.webp")
    }
