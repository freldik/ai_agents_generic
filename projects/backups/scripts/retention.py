"""Retence RAR archivů — drží 4 nejnovější + 1 na každý kalendářní rok.

Dohoda z 2026-08-10. Bez `--delete` **nic nemaže**, jen vypíše, co by smazal.

Pravidlo pro každou kategorii zvlášť (Others, Projects, …):
  - poslední 4 archivy se drží vždy
  - z každého kalendářního roku se navíc drží ten nejnovější
  - všechno ostatní je ke smazání

Skript pracuje jen v `D:\\Work\\Backup\\Data`, jinam nesahá. Datum bere z názvu
souboru (`Nazev_YYMMDD.rar`), ne z času modifikace — kopírování soubor "omladí".

Spuštění:
  .\\.venv\\Scripts\\python.exe projects/backups/scripts/retention.py
  ... --delete       opravdu smaže (zeptá se)
  ... --out <soubor> zapíše výpis i do souboru (pro naplánovanou úlohu)
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

DATA_DIR = Path("D:/Work/Backup/Data")
KEEP_RECENT = 4
NAME_RE = re.compile(r"^(?P<cat>.+)_(?P<stamp>\d{6})\.rar$", re.IGNORECASE)


def parse(path: Path) -> tuple[str, date] | None:
    m = NAME_RE.match(path.name)
    if not m:
        return None
    stamp = m.group("stamp")
    try:
        when = date(2000 + int(stamp[:2]), int(stamp[2:4]), int(stamp[4:6]))
    except ValueError:
        return None
    return m.group("cat"), when


def find_archives() -> dict[str, list[tuple[Path, date]]]:
    """Archivy podle kategorie — hledá i v podsložkách (nové rozložení) i v kořeni."""
    groups: dict[str, list[tuple[Path, date]]] = defaultdict(list)
    for path in DATA_DIR.rglob("*.rar"):
        parsed = parse(path)
        if parsed:
            groups[parsed[0]].append((path, parsed[1]))
    for items in groups.values():
        items.sort(key=lambda t: t[1], reverse=True)
    return groups


def split(items: list[tuple[Path, date]]) -> tuple[list, list]:
    """Rozdělí na (držet, smazat) podle pravidla 4 nejnovější + 1 na rok."""
    keep_paths = {p for p, _ in items[:KEEP_RECENT]}
    by_year: dict[int, tuple[Path, date]] = {}
    for path, when in items:  # items jsou sestupně, první v roce je ten nejnovější
        by_year.setdefault(when.year, (path, when))
    keep_paths |= {p for p, _ in by_year.values()}
    keep = [(p, d) for p, d in items if p in keep_paths]
    drop = [(p, d) for p, d in items if p not in keep_paths]
    return keep, drop


def mb(path: Path) -> float:
    return path.stat().st_size / 1024 / 1024


_lines: list[str] = []


def out(text: str = "") -> None:
    """Vypíše a zároveň si to pamatuje pro případný zápis do souboru (--out)."""
    print(text)
    _lines.append(text)


def write_report() -> None:
    if "--out" not in sys.argv:
        return
    idx = sys.argv.index("--out")
    if idx + 1 >= len(sys.argv):
        print("Chybí cesta za --out")
        return
    target = Path(sys.argv[idx + 1])
    target.parent.mkdir(parents=True, exist_ok=True)
    header = f"# Retence RAR archivů — {date.today().isoformat()}"
    target.write_text("\n".join([header, ""] + _lines) + "\n", encoding="utf-8")
    print(f"Zapsáno: {target}")


def main() -> None:
    if not DATA_DIR.exists():
        print(f"Neexistuje: {DATA_DIR}")
        sys.exit(1)

    groups = find_archives()
    if not groups:
        out(f"Žádné archivy `*_YYMMDD.rar` v {DATA_DIR}")
        write_report()
        return

    to_delete: list[Path] = []
    freed = 0.0
    for cat in sorted(groups):
        keep, drop = split(groups[cat])
        out(f"\n== {cat}  ({len(groups[cat])} archivů)")
        for path, when in keep:
            out(f"   držet  {when}  {mb(path):>9.0f} MB  {path.name}")
        for path, when in drop:
            out(f"   SMAZAT {when}  {mb(path):>9.0f} MB  {path.name}")
            to_delete.append(path)
            freed += mb(path)

    out(f"\nKe smazání: {len(to_delete)} souborů, {freed / 1024:.1f} GB")
    write_report()
    if not to_delete:
        return
    if "--delete" not in sys.argv:
        print("Nic se nesmazalo. Opravdové smazání: přidej `--delete`.")
        return

    answer = input(f"Opravdu smazat {len(to_delete)} archivů? napiš 'smazat': ")
    if answer.strip().lower() != "smazat":
        print("Zrušeno, nic se nesmazalo.")
        return
    for path in to_delete:
        path.unlink()
        print(f"smazáno: {path}")
    print(f"Uvolněno {freed / 1024:.1f} GB.")


if __name__ == "__main__":
    main()
