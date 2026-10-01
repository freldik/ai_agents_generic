"""Kostra skriptu projektu — ukazuje, jak se dostat ke sdíleným knihovnám."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.lib.repo import data_dir, dated, temp_dir  # noqa: E402

PROJECT = Path(__file__).resolve().parents[1].name


def main() -> None:
    print(f"Projekt: {PROJECT}")
    print(f"Data:    {data_dir(PROJECT)}")
    print(f"Výstup by šel do: {temp_dir(PROJECT) / dated('vystup', '.xlsx')}")


if __name__ == "__main__":
    main()
