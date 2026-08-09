"""Orientace v repozitáři a import sdílených knihoven ze skriptů projektů."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path


def repo_root() -> Path:
    """Kořen repa — hledá se nahoru podle přítomnosti .git."""
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Kořen repozitáře nenalezen (chybí .git)")


def ensure_on_path() -> None:
    """Přidá kořen repa do sys.path, aby šlo `from shared.lib import ...`."""
    root = str(repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def project_dir(name: str) -> Path:
    return repo_root() / "projects" / name


def data_dir(name: str) -> Path:
    d = project_dir(name) / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def dated(stem: str, suffix: str, on: date | None = None) -> str:
    """`dated("portfolio", ".xlsx")` -> `portfolio_2026-08-08.xlsx`."""
    return f"{stem}_{(on or date.today()).isoformat()}{suffix}"
