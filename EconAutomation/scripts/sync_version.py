#!/usr/bin/env python3
"""
Sync the version string from _version.py → version.json and pyproject.toml.

Run manually after editing _version.py:
    python scripts/sync_version.py

Or let the .githooks/pre-commit hook call it automatically whenever
_version.py is staged for a commit.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
_VERSION_FILE = ROOT / "src" / "econ_automation" / "_version.py"
_VERSION_JSON = ROOT / "version.json"
_PYPROJECT = ROOT / "pyproject.toml"
_DOWNLOAD_URL_TEMPLATE = (
    "https://github.com/ebusseyst/EconAutomation-REP"
    "/releases/download/v{version}/EconAutomation.exe"
)


def read_version() -> str:
    text = _VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        sys.exit(f"Could not parse __version__ from {_VERSION_FILE}")
    return match.group(1)


def update_version_json(version: str) -> None:
    existing = json.loads(_VERSION_JSON.read_text(encoding="utf-8"))
    existing["version"] = version
    existing["download_url"] = _DOWNLOAD_URL_TEMPLATE.format(version=version)
    _VERSION_JSON.write_text(json.dumps(existing, indent=4) + "\n", encoding="utf-8")
    print(f"  version.json      -> {version}")


def update_pyproject(version: str) -> None:
    text = _PYPROJECT.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r'^(version\s*=\s*)["\'][^"\']*["\']',
        lambda m: f'{m.group(1)}"{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        print("  pyproject.toml    — version field not found, skipping")
        return
    if new_text == text:
        print("  pyproject.toml    — already up to date")
        return
    _PYPROJECT.write_text(new_text, encoding="utf-8")
    print(f"  pyproject.toml    -> {version}")


if __name__ == "__main__":
    version = read_version()
    print(f"Syncing version {version!r} ...")
    update_version_json(version)
    update_pyproject(version)
    print("Done.")
