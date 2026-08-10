"""Stav záloh — co je aktuální a co je po termínu.

Pro každou položku z `config.json` najde nejnovější soubor v cílové složce
a porovná jeho datum s dohodnutým intervalem. Jen čte.

Spuštění:  .\\.venv\\Scripts\\python.exe projects/backups/scripts/status.py
           ... --md   zapíše report do data/status_RRRR-MM-DD.md
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.lib.repo import data_dir, dated  # noqa: E402

PROJECT_DIR = Path(__file__).resolve().parents[1]
PROJECT = PROJECT_DIR.name

OK, STARE, PO_TERMINU, CHYBI = "ok", "stárne", "PO TERMÍNU", "CHYBÍ"


def load_config() -> dict:
    return json.loads((PROJECT_DIR / "config.json").read_text(encoding="utf-8"))


def newest_file(folder: Path, pattern: str) -> tuple[Path | None, date | None]:
    """Nejnovější soubor odpovídající vzoru — podle času modifikace."""
    if not folder.exists():
        return None, None
    candidates = [p for p in folder.glob(pattern) if p.is_file()]
    if not candidates:
        return None, None
    newest = max(candidates, key=lambda p: p.stat().st_mtime)
    return newest, datetime.fromtimestamp(newest.stat().st_mtime).date()


def classify(age_days: int | None, interval: int) -> str:
    if age_days is None:
        return CHYBI
    if age_days > interval:
        return PO_TERMINU
    if age_days > interval * 0.8:
        return STARE
    return OK


def collect(config: dict) -> list[dict]:
    today = date.today()
    rows = []
    for item in config["items"]:
        folder = Path(item["kontrola"])
        newest, when = newest_file(folder, item["glob"])
        age = (today - when).days if when else None
        rows.append(
            {
                "id": item["id"],
                "nazev": item["nazev"],
                "interval": item["interval_dnu"],
                "posledni": when.isoformat() if when else "—",
                "vek_dnu": age,
                "stav": classify(age, item["interval_dnu"]),
                "soubor": str(newest) if newest else f"(nic v {folder})",
            }
        )
    return rows


def print_table(rows: list[dict]) -> None:
    order = {PO_TERMINU: 0, CHYBI: 1, STARE: 2, OK: 3}
    rows = sorted(rows, key=lambda r: (order[r["stav"]], -(r["vek_dnu"] or 0)))
    print(f"{'stav':<11} {'id':<16} {'poslední':<12} {'věk':>6} {'interval':>9}  co")
    print("-" * 88)
    for r in rows:
        vek = f"{r['vek_dnu']} d" if r["vek_dnu"] is not None else "—"
        print(
            f"{r['stav']:<11} {r['id']:<16} {r['posledni']:<12} "
            f"{vek:>6} {str(r['interval']) + ' d':>9}  {r['nazev']}"
        )
    problems = [r for r in rows if r["stav"] in (PO_TERMINU, CHYBI)]
    print()
    if problems:
        print(f"Vyžaduje pozornost: {len(problems)} z {len(rows)}")
        for r in problems:
            print(f"  - {r['id']}: {r['stav'].lower()} — {r['soubor']}")
    else:
        print(f"Všech {len(rows)} položek je v intervalu.")


def write_md(rows: list[dict]) -> Path:
    lines = [
        f"# Stav záloh — {date.today().isoformat()}",
        "",
        "> Generuje `scripts/status.py`. Definice položek v `config.json`,",
        "> vysvětlení v `data/inventory.md`.",
        "",
        "| Stav | id | Co | Poslední | Věk | Interval |",
        "|---|---|---|---|---|---|",
    ]
    order = {PO_TERMINU: 0, CHYBI: 1, STARE: 2, OK: 3}
    for r in sorted(rows, key=lambda r: order[r["stav"]]):
        vek = f"{r['vek_dnu']} d" if r["vek_dnu"] is not None else "—"
        lines.append(
            f"| {r['stav']} | `{r['id']}` | {r['nazev']} | {r['posledni']} "
            f"| {vek} | {r['interval']} d |"
        )
    target = data_dir(PROJECT) / dated("status", ".md")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def main() -> None:
    rows = collect(load_config())
    print_table(rows)
    if "--md" in sys.argv:
        print(f"\nZapsáno: {write_md(rows)}")


if __name__ == "__main__":
    main()
