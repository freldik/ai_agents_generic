# Projekt: stocks-tracker

## Účel

Sledování akciového portfolia — držené pozice, aktuální ceny, vývoj hodnoty v čase.
Výstupem je Excel přehled a snapshoty pro historii.

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `data/portfolio.csv` | držené pozice: ticker, počet kusů, nákupní cena, datum, měna | ručně udržováno uživatelem |
| `data/snapshots/` | denní/týdenní snapshoty hodnoty portfolia | generuje `snapshot.py` |

`portfolio.csv` je **zdroj pravdy a upravuje ho jen uživatel.** Skripty z něj jen čtou.

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/snapshot.py` | stáhne aktuální ceny (yfinance), spočítá hodnotu a zisk/ztrátu, uloží snapshot |

Spuštění z kořene repa:
`.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/snapshot.py`

## Pravidla specifická pro tento projekt

- **Toto není investiční poradenství.** Skripty počítají čísla, nedoporučují obchody.
  Když se uživatel ptá „mám prodat?", odpověz čísly a riziky, ne doporučením.
- Ceny z yfinance jsou **zpožděné** a občas vrátí `NaN` u méně likvidních tickerů —
  chybějící cenu hlas, nedosazuj poslední známou bez upozornění.
- Nákupní ceny jsou v měně uvedené ve sloupci `currency`. Přepočet na CZK dělej
  jen když o to uživatel požádá, a vždy uveď použitý kurz a jeho datum.
- Snapshoty se nikdy nepřepisují — jeden soubor na datum.

## Otevřené otázky

- Zahrnout dividendy do výnosu? Zatím ne.
- Zdroj kurzu CZK/USD pro přepočty — zatím nevybrán.
