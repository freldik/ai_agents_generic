# Projekt: stocks-tracker

## Účel

Sledování akciového portfolia u brokera XTB — kolik je do které akcie investováno,
jakou má dnes hodnotu a kolik ještě zbývá dokoupit do plánu.

Přehled se drží v ručním excelu **`D:\Work\Finance\Test\sporeni.xlsx`** (mimo tento repozitář).
Úkolem projektu je přenášet do něj čísla z exportu portfolia z XTB, aby se
nepřepisovala ručně.

## Kde jsou držené akcie

**Zdroj pravdy o pozicích je broker**, ne tento repozitář. Sešit `sporeni.xlsx` je
ruční přehled nad tím — drží plán nákupů, kategorie a rozdělení podle vlastníka,
což u brokera není.

### Strom exportů

```
D:\Work\Finance\Test\            ← kořen (konstanta ROOT ve skriptu)
├─ sporeni.xlsx
├─ Marek\
│  └─ XTB\
│     └─ USD_51959804_2006-01-01_2026-08-13.xlsx
├─ Monika\
├─ Anetka\
└─ Adelka\
```

- **první úroveň = vlastník** → sloupec `Vlastnik` v sešitu
- **druhá úroveň = broker** → sloupec `Broker` v sešitu (zatím jen XTB)
- **soubory = měny**, poznají se podle předpony názvu: `USD_`, `EUR_`, `CZK_`

Ve složce brokera smí být pro každou měnu **právě jeden** soubor. Skript to kontroluje
a při dvou souborech téže měny skončí chybou — konkrétní název se proto nikde nezadává.
Starý export ze složky smaž, nebo ho odsuň jinam.

**Řádek, ke kterému v exportu není pozice, skript nepřepisuje** — jen ho vypíše
(v konzoli i v reportu, s aktuálními hodnotami). Platí to pro plánované nákupy,
pro řádky měny, pro kterou ve složce export není, i pro prodané pozice — ty je
potřeba vynulovat nebo smazat ručně. Vlastník, který nemá složku s exportem, se
**vůbec nedotkne**.

### List v sešitu

Všichni vlastníci jsou na **jednom společném listu `Akcie`** (tabulka `Tabulka2`
od `A1`). Jeden řádek = jedna pozice, určená sloupci `Vlastnik`, `Broker` a `Mena`.
Skript zpracuje jen řádky, které odpovídají složce a souboru, ze kterých export přišel:
`Marek\XTB\USD_*.xlsx` plní jen řádky s `Vlastnik=Marek`, `Broker=XTB`, `Mena=USD`.

**`Mena` = měna čísel v řádku**, ne měna burzy. Sešit podle ní bere kurz
(`VLOOKUP(Mena, Kurzy)`), takže USD částka v řádku s `Mena=EUR` by dala špatné CZK.
Účet XTB je v USD a přepočítává do USD i evropské tituly (Rheinmetall, voestalpine,
ArcelorMittal…) — ty proto patří do řádku s `Mena=USD`.

Párování řádku s pozicí v exportu:

1. **podle tickeru** — první část sloupce `Nazev akcie` před čárkou (`GOOGL.US, Alphabet…`),
2. u řádků **bez tickeru** podle názvu ve sloupci `Akcie` (normalizovaně, + `ALIASES`).

Řádek s tickerem se podle názvu nepáruje — plánované nákupy (např. `S&P 500` s `500U.UK`)
by jinak sebraly cizí pozici. Jedna pozice smí patřit jen jednomu řádku.

Sloupce se **hledají podle názvů v hlavičce**, ne podle písmen, a rozsah řádků se bere
z definice tabulky, aby skript nesáhl na tabulku měn a součty pod ní. Nepřejmenovávej
proto hlavičky `Akcie`, `Nazev akcie`, `Vlastnik`, `Broker`, `Mena`, `Investovano`, `Hodnota`.

**Vlastník musí mít na listu své řádky.** Když má export, ale ani jeden řádek s jeho
jménem ve sloupci `Vlastnik`, skript nezapíše nic a nahlásí to — v konzoli i v reportu:

```
Monika / XTB  →  list 'Akcie'
  exporty: USD   změněných řádků: 0 z 0
  !! na listu není jediný řádek s Vlastnik=Monika a Broker=XTB — nezapsalo se nic
```

Tohle je dnes stav Moniky, Anetky i Adélky: složky mají, řádky v sešitu ne.

Sloupce, o které jde:

| Sloupec | Kdo ho plní |
|---|---|
| Akcie, Nazev akcie (ticker, název), Kategorie, Typ, Broker, Vlastnik, Mena | ručně uživatel |
| Upozorneni prodej / nakup, Plan | ručně uživatel |
| **Investovano, Hodnota** | **`xtb_sync.py`** |
| Dokoupit, Zisk, Zisk %, Kurz, … CZK | vzorce |

Pod tabulkou akcií je tabulka měn `Tabulka3` (hotovost podle měny/brokera/vlastníka),
kurzy (`Kurzy` = `A60:B63`) a souhrny podle vlastníka, brokera a kategorie.
`xtb_sync.py` z toho nemění nic; kurzy (jen sloupec B oblasti `Kurzy`) přepisuje
`update_rates.py`.

Řádky bez otevřené pozice (CEZ, Colt CZ Group, EUR overnight Rate Swap, EUR varianty
Rheinmetallu a HeidelbergCementu, S&P 500 `500U.UK`) jsou plánované nákupy — skript
je jen vypíše a nechá, jak jsou.

## Postup aktualizace

### 1. Stáhnout export

xStation 5 (web) → **Historie účtu** → **Export**. Období od `2006-01-01` do dneška,
formát Excel. Soubor ulož do `<kořen>\<Vlastnik>\<Broker>\` a **starý odtud smaž**.

Podstatný je list **`Open Positions`**:

- řádky se **vyplněnou** kategorií (`STOCK`, `ETF`) = souhrn za instrument — z těch se čte
- řádky s **prázdnou** kategorií = jednotlivé nákupy, které se do souhrnu sčítají
- `Value` = dnešní hodnota, `Net Profit` = zisk → **investováno = `Value − Net Profit`**
  (sedí na `Volume × Open price`)

### 2. Nejdřív nasucho

```powershell
.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/xtb_sync.py --dry-run
```

Projde všechny vlastníky a brokery, vypíše změny a uloží report do
`temp/xtb_sync_dry-run_<datum>.md`. Do sešitu nezapíše nic.

**Zkontroluj v reportu:** sekci „pozice z exportu, které nemají řádek v sešitu“ — když
tam něco je, nově koupená akcie ještě nemá řádek a její peníze by se nikam nezapočítaly.

### 3. Zapsat

```powershell
.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/xtb_sync.py --write
```

Uloží report do `temp/xtb_sync_<datum>.md` a zálohu sešitu jako `sporeni.bak.xlsx`.
Report má sekci pro každou dvojici vlastník + broker: kontrolu součtů (hlavička exportu
vs. co se zapsalo), tabulku řádků (staré → nové) a seznam pozic bez řádku s nápovědou,
který řádek je nejspíš myšlen (jiný ticker / jiná Mena).

Sešit nesmí být při zápisu otevřený v Excelu — skript to pozná podle `~$sporeni.xlsx`
a skončí.

Přepínače: `--root` (jiný kořen exportů), `--sporeni` (jiný sešit, výchozí je
`<kořen>\sporeni.xlsx`), `--no-report`.

### 4. Aktualizovat kurzy

```powershell
.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/update_rates.py          # jen výpis
.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/update_rates.py --write
```

Stáhne denní kurz ČNB (`cnb.cz/.../denni_kurz.txt`) a přepíše sloupec B v pojmenované
oblasti `Kurzy` podle kódu měny ve sloupci A. CZK zůstává 1; měna, kterou ČNB
nevyhlašuje, se jen nahlásí. Kurz je přepočtený na 1 jednotku (ČNB uvádí např. JPY
za 100). O víkendu/svátku ČNB vrací poslední platný kurz — skript vypíše datum jeho
vyhlášení. `--date YYYY-MM-DD` vezme kurz k jinému dni.

### 5. Otevřít sešit v Excelu

Vzorce (Zisk, součty, přepočty do CZK) se přepočítají při otevření.

## Přidání vlastníka, brokera nebo měny

| Co přidáváš | Co udělat |
|---|---|
| **vlastníka** | složku `<kořen>\<Jmeno>\<Broker>\` s exportem **a** řádky na listu `Akcie` s jeho jménem ve sloupci `Vlastnik` |
| **brokera** | složku `<kořen>\<Vlastnik>\<NovyBroker>\` **a** řádky s `Broker=<NovyBroker>`; jiný formát exportu než XTB znamená upravit `read_export()` |
| **měnu** | soubor `EUR_*.xlsx` / `CZK_*.xlsx` do složky brokera **a** řádky s touto `Mena` |

Ve skriptu se nemusí měnit nic dalšího — vlastníci, brokeři i měny se hledají
procházením stromu. Jméno složky musí sedět na hodnotu ve sloupci (porovnává se
bez ohledu na velikost písmen a diakritiku).

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `D:\Work\Finance\Test\sporeni.xlsx` | přehled portfolia — **mimo repozitář** | ruční sešit uživatele |
| `…\Test\<Vlastnik>\<Broker>\<MENA>_*.xlsx` | exporty pozic — **mimo repozitář** | xStation 5 |
| `temp/xtb_sync_*.md` | co se při aktualizaci přepsalo — **neverzuje se** | generuje `xtb_sync.py` |
| `data/xtb_sync_2026-08-13.md` | report z prvního zápisu, ponechaný v historii | `xtb_sync.py` (starší verze) |
| `data/portfolio.csv` | **nepoužívá se** — ukázková data ze šablony (MSFT, CEZ.PR) | — |

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/xtb_sync.py` | přepíše Investovano a Hodnota v `sporeni.xlsx` podle exportu z XTB. Bez `--write` jen vypíše rozdíly. |
| `scripts/update_rates.py` | přepíše kurzy k CZK v oblasti `Kurzy` podle denního kurzu ČNB. Bez `--write` jen vypíše. |
| `scripts/_run.bat` + `sync_*.bat`, `kurzy_*.bat` | `.bat` obálky — dvojklik místo příkazové řádky, viz níže |
| `scripts/snapshot.py` | **nepoužívá se** — stahuje ceny přes yfinance k `portfolio.csv`. Zbytek šablony. |

### Spouštění bez příkazové řádky — `.bat` obálky

Stejný vzor jako v projektu `backups`. Dvojklik na obálku ve `scripts/` sama najde
venv, spustí skript z kořene repa, na konci vypíše `[OK]` / `[CHYBA]` a počká na klávesu.

| Dvojklik na | Spustí | Píše do sešitu? |
|---|---|---|
| `sync_nanecisto.bat` | `xtb_sync.py --dry-run` | ne (jen report do `temp/`) |
| `sync_zapsat.bat` | `xtb_sync.py --write` | **ano** — před během se ptá (pause) |
| `kurzy_nanecisto.bat` | `update_rates.py` | ne |
| `kurzy_zapsat.bat` | `update_rates.py --write` | **ano** — před během se ptá (pause) |

`_run.bat` je společný spouštěč (nespouštět přímo), přepne konzoli na UTF-8 kvůli
češtině. Nový skript = nová obálka s jedním `call "%~dp0_run.bat" <skript.py> <parametry>`.

**Odkazy mimo repo — `D:\Work\Skripty\Stocks-tracker\`.** Obálky z `scripts/` se
nesmí kopírovat jinam (kořen repa hledají tři úrovně nad sebou). Ve složce mimo repo
jsou proto stejnojmenné **odkazy**, které jen zavolají obálku v repu. Cesta k repu
je jen v `_cesta.bat` v té složce — po přesunu repa se upraví jen tam. Složka se
neverzuje (absolutní cesta ke stroji); nový skript = nový odkaz podle vzoru.

## Pravidla specifická pro tento projekt

- **Toto není investiční poradenství.** Skripty počítají čísla, nedoporučují obchody.
  Když se uživatel ptá „mám prodat?", odpověz čísly a riziky, ne doporučením.
- Nákupní ceny jsou v měně uvedené ve sloupci `currency`. Přepočet na CZK dělej
  jen když o to uživatel požádá, a vždy uveď použitý kurz a jeho datum.

### Práce se `sporeni.xlsx`

- **Nikdy ho neotvírej a neukládej přes openpyxl ani pandas.** Má 10 grafů, tabulky
  a webextension, které přepis zahodí. `xtb_sync.py` proto zapisuje hodnoty přímo
  do XML uvnitř `.xlsx` a předtím dělá `.bak.xlsx` zálohu.
- Měnit se smí **jen** sloupce Investovano a Hodnota na řádcích tabulky akcií
  (`xtb_sync.py`) a sloupec B oblasti `Kurzy` (`update_rates.py`). Všechno ostatní je
  uživatelovo — plán, kategorie, vzorce, součty pod tabulkou, ostatní listy.
- Sloupce se hledají podle **názvů v hlavičce**, řádky podle rozsahu tabulky. Nikdy
  je nezadávej natvrdo písmeny — každý vlastník má list jinak.
- Účet u XTB je vedený v jedné měně, takže jeden export plní jen řádky s touto `Mena`;
  řádky jiné měny zůstanou beze změny, dokud pro ně nepřibude vlastní export.
- Zaokrouhluje se na celá čísla — sešit tak má hodnoty od začátku.
- **Kontrola po běhu:** součet sloupce Hodnota v dané měně musí sedět na
  `My Trades / Value` z hlavičky listu `Open Positions`. K 2026-08-13 to bylo 39 224 USD.
- Páruje se podle tickeru ve sloupci `Nazev akcie`. Jen u řádků bez tickeru podle
  názvu; když se název v exportu liší víc, patří dvojice do `ALIASES` ve skriptu.

## Otevřené otázky

- Zahrnout dividendy do výnosu? Zatím ne.
- Řádek `NasdaQ` má kategorii „Fond", ale páruje se na `NDAQ.US`, což je akcie burzy
  Nasdaq, ne indexový fond. Ověřit, jestli je to zamýšlené.
- Monika, Anetka a Adélka mají složky, ale **žádné řádky na listu `Akcie`**. Dokud
  je nepřidáš (s vyplněným `Vlastnik` a `Broker`), jejich exporty se nikam nezapíšou —
  skript to jen nahlásí.
- Smazat nepoužívané `portfolio.csv` a `snapshot.py`, nebo je nechat jako kostru?
