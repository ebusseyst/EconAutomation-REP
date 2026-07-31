import json
import logging
import os
import platform
from pathlib import Path

logger = logging.getLogger(__name__)

_CACHE_FILE = "case_info_cache.json"


def _cache_path() -> Path:
    if platform.system() == "Windows":
        return (
            Path(os.environ.get("LOCALAPPDATA", Path.home()))
            / "EconAutomation"
            / _CACHE_FILE
        )
    return (
        Path.home() / "Library" / "Application Support" / "EconAutomation" / _CACHE_FILE
    )


def save_case_info(data: dict) -> None:
    path = _cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        logger.exception("case_info_persistence: failed to save case info cache")


def load_case_info() -> dict | None:
    path = _cache_path()
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("case_info_persistence: failed to load case info cache")
    return None
