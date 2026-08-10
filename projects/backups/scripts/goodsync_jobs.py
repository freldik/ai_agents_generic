"""Vytáhne seznam GoodSync jobů z `jobs.tic` a zapíše ho jako markdown tabulku.

`%APPDATA%\\GoodSync\\jobs.tic` je textový soubor s jedním jobem na řádek ve formátu
délkou prefixovaných polí:

    [n:16:Projects - Cloud|0[r:11:D:\\Projects|...]1[r:26:M:\\Backup\\Desktop\\Projects|...]...

`n` = jméno jobu, blok `0[` = levá strana, blok `1[` = pravá strana, pole `r` = cesta.
Čísla jsou délky v bajtech, takže se nedá spoléhat na dělení podle `|` — název i cesta
můžou svislítko obsahovat. Proto se čte přesně podle délky.

Poslední časy běhů v `jobs.tic` **nejsou** — ty jsou jen v GUI GoodSyncu.
Ručně opsaný stav je v `data/goodsync_runs_*.md`.

Spuštění:  .\\.venv\\Scripts\\python.exe projects/backups/scripts/goodsync_jobs.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.lib.repo import data_dir, dated  # noqa: E402

PROJECT_DIR = Path(__file__).resolve().parents[1]
PROJECT = PROJECT_DIR.name
CONFIG = json.loads((PROJECT_DIR / "config.json").read_text(encoding="utf-8"))

# Pravá strana -> lidský popis cíle. Podle dohody s uživatelem.
TARGETS = [
    ("M:\\", "WD MyCloud (síťový disk)"),
    ("=My Passport", "USB disk My Passport"),
    ("N:\\", "pracovní notebook"),
    ("L:\\", "notebook Moniky"),
    ("D:\\OneDrive", "OneDrive"),
    ("D:\\Work\\Backup", "lokální shromaždiště D:\\Work\\Backup"),
    ("P:\\", "WD MyCloud — Public"),
]


def read_field(text: str, pos: int, key: str) -> tuple[str, int] | None:
    """Přečte pole `<key>:<délka>:<hodnota>` na pozici `pos`. Vrací (hodnota, konec)."""
    prefix = f"{key}:"
    if not text.startswith(prefix, pos):
        return None
    colon = text.index(":", pos + len(prefix))
    length = int(text[pos + len(prefix) : colon])
    start = colon + 1
    return text[start : start + length], start + length


def first_field(line: str, key: str, search_from: int = 0) -> str | None:
    """Najde první výskyt pole `key` od dané pozice a vrátí jeho hodnotu."""
    pos = search_from
    while True:
        pos = line.find(f"{key}:", pos)
        if pos == -1:
            return None
        got = read_field(line, pos, key)
        if got:
            return got[0]
        pos += 1


def parse_jobs(path: Path) -> list[dict]:
    jobs = []
    for line in path.read_text(encoding="latin-1").splitlines():
        if not line.startswith("[n:"):
            continue
        name, after_name = read_field(line, 1, "n")
        left_block = line.find("[", after_name)
        right_block = line.find("]1[", left_block)
        left = first_field(line, "r", left_block)
        right = first_field(line, "r", right_block) if right_block != -1 else None
        jobs.append({"name": name, "left": left or "?", "right": right or "?"})
    return jobs


def describe_target(right: str) -> str:
    for prefix, label in TARGETS:
        if right.startswith(prefix):
            return label
    return "neznámý cíl"


def main() -> None:
    jobs_tic = Path(CONFIG["zdroje_konfiguraci"]["goodsync"]) / "jobs.tic"
    if not jobs_tic.exists():
        print(f"Nenalezeno: {jobs_tic}")
        sys.exit(1)

    jobs = parse_jobs(jobs_tic)
    lines = [
        f"# GoodSync joby — {dated('', '').strip('_')}",
        "",
        f"> Generuje `scripts/goodsync_jobs.py` z `{jobs_tic}`.",
        "> Poslední časy běhů tady nejsou — ty jsou jen v GUI, viz `goodsync_runs_*.md`.",
        "",
        f"Celkem jobů: **{len(jobs)}**",
        "",
        "| Job | Odkud | Kam | Cíl |",
        "|---|---|---|---|",
    ]
    for job in sorted(jobs, key=lambda j: (describe_target(j["right"]), j["name"])):
        lines.append(
            f"| {job['name']} | `{job['left']}` | `{job['right']}` "
            f"| {describe_target(job['right'])} |"
        )

    unknown = [j for j in jobs if describe_target(j["right"]) == "neznámý cíl"]
    if unknown:
        lines += ["", "## Nezařazené cíle", ""]
        lines += [f"- {j['name']} -> `{j['right']}`" for j in unknown]

    target = data_dir(PROJECT) / dated("goodsync_jobs", ".md")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Zapsáno: {target}  ({len(jobs)} jobů, {len(unknown)} nezařazených)")


if __name__ == "__main__":
    main()
