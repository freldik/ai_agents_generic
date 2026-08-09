"""Bezpečné čtení a zápis .xlsx.

Zásada: vstupní soubory se nikdy nepřepisují. Zápis buď přidává list do kopie,
nebo píše nový soubor s datem v názvu.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd


def read_sheet(path: str | Path, sheet: str | int = 0) -> pd.DataFrame:
    """Načte jeden list. Prázdné řádky/sloupce se zahodí."""
    df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    return df.dropna(how="all").dropna(axis=1, how="all")


def read_all(path: str | Path) -> dict[str, pd.DataFrame]:
    return pd.read_excel(path, sheet_name=None, engine="openpyxl")


def write_new(df: pd.DataFrame, path: str | Path, sheet: str = "Data") -> Path:
    """Zapíše DataFrame do nového souboru s automatickou šířkou sloupců."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="xlsxwriter") as xl:
        df.to_excel(xl, sheet_name=sheet, index=False)
        ws = xl.sheets[sheet]
        for i, col in enumerate(df.columns):
            width = max(len(str(col)), *(df[col].astype(str).str.len().tolist() or [0]))
            ws.set_column(i, i, min(width + 2, 50))
    return path


def append_sheet(df: pd.DataFrame, path: str | Path, sheet: str) -> Path:
    """Přidá list do existujícího sešitu; ostatní listy a jejich formátování zůstanou.

    Existující list stejného jména je nahrazen. Původní soubor se nejdřív zálohuje
    jako `<jmeno>.bak.xlsx`.
    """
    path = Path(path)
    if not path.exists():
        return write_new(df, path, sheet)
    shutil.copy2(path, path.with_suffix(".bak.xlsx"))
    with pd.ExcelWriter(
        path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as xl:
        df.to_excel(xl, sheet_name=sheet, index=False)
    return path
