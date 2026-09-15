from __future__ import annotations

from io import BytesIO
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

from PIL import Image


CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "images"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(key: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in key).strip("_") or "image"


def load_image_async(url: str | None, key: str, size: tuple[int, int], on_ready):
    """Load an image from local cache or Game8 in the background.

    on_ready(PIL.Image.Image | None) is called from the worker thread; callers
    should marshal UI changes back to Tk with `after(0, ...)`.
    """
    if not url:
        on_ready(None)
        return

    path = CACHE_DIR / f"{_safe_name(key)}.png"

    def worker():
        try:
            if path.exists():
                image = Image.open(path).convert("RGBA")
            else:
                request = Request(url, headers={"User-Agent": "Mozilla/5.0 MHS3 Companion"})
                with urlopen(request, timeout=12) as response:
                    raw = response.read()
                image = Image.open(BytesIO(raw)).convert("RGBA")
                image.save(path, "PNG")
            image.thumbnail(size, Image.Resampling.LANCZOS)
            on_ready(image)
        except Exception:
            on_ready(None)

    Thread(target=worker, daemon=True).start()
