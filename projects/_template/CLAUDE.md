# Projekt: <NÁZEV>

> Kostra nového projektu. Zkopíruj celou složku `projects/_template/` pod nové jméno
> a vyplň sekce níže. Nic mimo novou složku se měnit nemá.

## Účel

<Jednou až třemi větami: co tento projekt dělá a proč existuje.>

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `data/…` | | |

Vstupní data se **nepřepisují**. Výstupy skriptů jdou do `temp/` s datem v názvu
(`temp_dir()` ze `shared.lib.repo`) — `temp/` se neverzuje, `data/` ano.

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/…` | |

Spouštění z kořene repa:
`.\.venv\Scripts\python.exe projects/<name>/scripts/<script>.py`

## Pravidla specifická pro tento projekt

- <např. „Částky jsou v CZK, pokud sloupec neříká jinak.">

## Otevřené otázky

- <co ještě není rozhodnuté>
