---
name: excel-io
description: Čtení a zápis .xlsx souborů v tomto repu — nákupní seznamy, portfolio, jakákoli tabulková data. Použij vždy, když má úloha číst nebo produkovat Excel, CSV nebo tabulku.
---

# Práce s Excelem

## Vždy použij `shared/lib/excel_io.py`

Neimplementuj čtení/zápis znovu. Ze skriptu v projektu:

```python
from shared.lib.repo import ensure_on_path, data_dir, dated, temp_dir
ensure_on_path()
from shared.lib import excel_io

df = excel_io.read_sheet(data_dir("groceries") / "nakupy.xlsx", sheet="2026")
excel_io.write_new(vysledek, temp_dir("groceries") / dated("souhrn", ".xlsx"))
```

Vstupy čti z `data/` (verzuje se), výstupy skriptů piš do `temp/` (neverzuje se).

- `read_sheet(path, sheet)` — jeden list, prázdné řádky/sloupce odstraněny
- `read_all(path)` — dict všech listů
- `write_new(df, path, sheet)` — nový soubor, auto šířka sloupců
- `append_sheet(df, path, sheet)` — přidá list do existujícího sešitu, zbytek nechá být, dělá `.bak.xlsx` zálohu

## Pravidla

1. **Nikdy nepřepisuj vstupní soubor.** Uživatel v něm má ruční úpravy a formátování,
   které pandas při přepsání zahodí. Piš do `temp/` (`dated()`) nebo přidej list.
2. **Před zápisem do existujícího souboru se zeptej.**
3. **Datumy** parsuj do `datetime`, ukládej jako datum (ne string). V názvech souborů `YYYY-MM-DD`.
4. **Čísla s čárkou** — české Excely mívají desetinnou čárku a `1 234,50`.
   Před výpočtem převeď: `s.str.replace(" ", "").str.replace(",", ".").astype(float)`.
5. **Měny neslučuj naslepo.** Pokud tabulka míchá CZK/USD, zeptej se na kurz nebo ho dohledej.

## Než začneš počítat

Přečti si nejdřív hlavičku a pár řádků (`df.head()`, `df.dtypes`) a shrň uživateli,
jak jsi tabulku pochopil. Reálné domácí tabulky mají spojené buňky, mezisoučty
uprostřed dat a překlepy v názvech sloupců — nespoléhej na to, že struktura je čistá.
