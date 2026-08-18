# Projekt: stocks-tracker

## Účel

Sledování akciového portfolia u brokera XTB — kolik je do které akcie investováno,
jakou má dnes hodnotu a kolik ještě zbývá dokoupit do plánu.

Přehled se drží v ručním excelu **`D:\Work\Sporeni\sporeni.xlsx`** (mimo tento repozitář).
Úkolem projektu je přenášet do něj čísla z exportu portfolia z XTB, aby se
nepřepisovala ručně.

## Kde jsou držené akcie

**Zdroj pravdy o pozicích je broker**, ne tento repozitář. Sešit `sporeni.xlsx` je
ruční přehled nad tím — drží plán nákupů, kategorie a rozdělení podle vlastníka,
což u brokera není.

### Strom exportů

```
D:\Work\Sporeni\Test\            ← kořen (konstanta ROOT ve skriptu)
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

Měna, pro kterou ve složce export není, se zapíše jako **0** — čte se to jako „v téhle
měně u tohohle brokera nic nedržím“. Vlastník, který nemá složku s exportem, se
**vůbec nedotkne** — jeho list zůstane, jak je.

### List v sešitu

Všichni vlastníci jsou na **jednom společném listu `Akcie`** a rozlišují se sloupci
`Vlastnik` a `Broker`. Skript zpracuje jen řádky, které odpovídají složce, ze které
export přišel — `Marek\XTB\` sáhne jen na řádky s `Vlastnik=Marek` a `Broker=XTB`.

Jak se list hledá:

1. Je-li v sešitu list se sloupci `Vlastnik` **i** `Broker`, je to společný list a patří
   do něj všichni. (Dnešní stav — list `Akcie`.)
2. Jinak se hledá list pojmenovaný `Akcie - <Broker> (<Vlastnik>)`. Tuhle podobu měl
   sešit dřív; kdyby se k ní vrátil, skript ji pozná. Markův list se tehdy jmenoval
   `Akcie - XTB (Moje)` — výjimku řeší `OWNER_ALIASES` ve skriptu.

Sloupce se **hledají podle názvů v hlavičce**, ne podle písmen, a rozsah řádků se bere
z definice tabulky, aby skript nesáhl na součty pod ní. Nepřejmenovávej proto hlavičky
`Investovano USD`, `Hodnota EUR` atd.

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
| Akcie, Kategorie, Broker, Vlastnik | ručně uživatel |
| **Investovano USD / EUR / CZK** | **`xtb_sync.py`** |
| Plan — kolik chce uživatel do titulu vložit | ručně uživatel |
| Dokoupit | vzorec `MAX(0, Plan − Investovano)` |
| **Hodnota USD / EUR / CZK** | **`xtb_sync.py`** |
| Zisk a Zisk % ve všech měnách | vzorce |

Pod tabulkou akcií je ještě tabulka měn (ř. 51–53), součty (55–59), kurzy `C61`/`C62`
a souhrn podle vlastníka (66+, `SUMIF` přes sloupec `Vlastnik`). **Nic z toho skript
nemění** — souhrn se dopočítá sám, jakmile přibudou řádky dalších vlastníků.

Řádky bez otevřené pozice (CEZ, Colt CZ Group, II EUR overnight Rate Swap) jsou
plánované nákupy a zůstávají na nule.

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
`data/xtb_sync_dry-run_<datum>.md`. Do sešitu nezapíše nic.

**Zkontroluj v reportu:** sekci „pozice z exportu, které nemají řádek v sešitu“ — když
tam něco je, nově koupená akcie ještě nemá řádek a její peníze by se nikam nezapočítaly.

### 3. Zapsat

```powershell
.\.venv\Scripts\python.exe projects/stocks-tracker/scripts/xtb_sync.py --write
```

Uloží report do `data/xtb_sync_<datum>.md` a zálohu sešitu jako `sporeni.bak.xlsx`.
Report má sekci pro každou dvojici vlastník + broker a v každé tabulku se všemi třemi
měnami vedle sebe (staré → nové), včetně součtového řádku.

Přepínače: `--root` (jiný kořen exportů), `--sporeni` (jiný sešit, výchozí je
`<kořen>\sporeni.xlsx`), `--no-report`.

### 4. Otevřít sešit v Excelu

Vzorce (Zisk, součty, přepočty do CZK) se přepočítají při otevření.
Kurzy v `C61`/`C62` si uživatel aktualizuje sám — skript na ně nesahá.

## Přidání vlastníka, brokera nebo měny

| Co přidáváš | Co udělat |
|---|---|
| **vlastníka** | složku `<kořen>\<Jmeno>\<Broker>\` s exportem **a** řádky na listu `Akcie` s jeho jménem ve sloupci `Vlastnik` |
| **brokera** | složku `<kořen>\<Vlastnik>\<NovyBroker>\` **a** řádky s `Broker=<NovyBroker>`; jiný formát exportu než XTB znamená upravit `read_export()` |
| **měnu** | jen přidat do složky brokera soubor `EUR_*.xlsx` / `CZK_*.xlsx` |

Ve skriptu se nemusí měnit nic dalšího — vlastníci, brokeři i měny se hledají
procházením stromu. Jméno složky musí sedět na hodnotu ve sloupci (porovnává se
bez ohledu na velikost písmen a diakritiku).

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `D:\Work\Sporeni\Test\sporeni.xlsx` | přehled portfolia — **mimo repozitář** | ruční sešit uživatele |
| `…\Test\<Vlastnik>\<Broker>\<MENA>_*.xlsx` | exporty pozic — **mimo repozitář** | xStation 5 |
| `data/xtb_sync_*.md` | co se při aktualizaci přepsalo, po vlastnících a brokerech, všechny měny | generuje `xtb_sync.py` |
| `data/portfolio.csv` | **nepoužívá se** — ukázková data ze šablony (MSFT, CEZ.PR) | — |

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/xtb_sync.py` | přepíše Investovano a Hodnota v `sporeni.xlsx` podle exportu z XTB. Bez `--write` jen vypíše rozdíly. |
| `scripts/snapshot.py` | **nepoužívá se** — stahuje ceny přes yfinance k `portfolio.csv`. Zbytek šablony. |

## Pravidla specifická pro tento projekt

- **Toto není investiční poradenství.** Skripty počítají čísla, nedoporučují obchody.
  Když se uživatel ptá „mám prodat?", odpověz čísly a riziky, ne doporučením.
- Nákupní ceny jsou v měně uvedené ve sloupci `currency`. Přepočet na CZK dělej
  jen když o to uživatel požádá, a vždy uveď použitý kurz a jeho datum.

### Práce se `sporeni.xlsx`

- **Nikdy ho neotvírej a neukládej přes openpyxl ani pandas.** Má 10 grafů, tabulky
  a webextension, které přepis zahodí. `xtb_sync.py` proto zapisuje hodnoty přímo
  do XML uvnitř `.xlsx` a předtím dělá `.bak.xlsx` zálohu.
- Měnit se smí **jen** sloupce Investovano a Hodnota v USD/EUR/CZK, a jen na řádcích
  tabulky akcií. Všechno ostatní je uživatelovo — plán, kategorie, kurzy, vzorce,
  součty pod tabulkou, ostatní listy.
- Sloupce se hledají podle **názvů v hlavičce**, řádky podle rozsahu tabulky. Nikdy
  je nezadávej natvrdo písmeny — každý vlastník má list jinak.
- Účet u XTB je vedený v jedné měně, takže z jednoho exportu se plní jen jedna trojice
  sloupců; ostatní měny jdou na 0, dokud pro ně nepřibude vlastní export. Platí to
  i pro evropské tituly (Rheinmetall, voestalpine, SAAB, EURO STOXX 50) — XTB je
  přepočítává do měny účtu.
- Zaokrouhluje se na celá čísla — sešit tak má hodnoty od začátku.
- **Kontrola po běhu:** součet sloupce Hodnota v dané měně musí sedět na
  `My Trades / Value` z hlavičky listu `Open Positions`. K 2026-08-13 to bylo 39 224 USD.
- Páruje se podle názvu akcie (normalizovaně, bez mezer a diakritiky). Když se název
  v exportu liší víc, patří dvojice do `ALIASES` ve skriptu — **ne přejmenování
  řádku v sešitu**.

## Otevřené otázky

- Zahrnout dividendy do výnosu? Zatím ne.
- Zdroj kurzu CZK/USD pro přepočty — zatím nevybrán, kurzy se zadávají ručně.
- Řádek `NasdaQ` má kategorii „Fond", ale páruje se na `NDAQ.US`, což je akcie burzy
  Nasdaq, ne indexový fond. Ověřit, jestli je to zamýšlené.
- Monika, Anetka a Adélka mají složky, ale **žádné řádky na listu `Akcie`**. Dokud
  je nepřidáš (s vyplněným `Vlastnik` a `Broker`), jejich exporty se nikam nezapíšou —
  skript to jen nahlásí.
- Smazat nepoužívané `portfolio.csv` a `snapshot.py`, nebo je nechat jako kostru?
