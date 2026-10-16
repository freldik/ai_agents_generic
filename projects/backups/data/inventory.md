# Inventura záloh

Zjištěno průzkumem stroje 2026-08-10 (`discovery_2026-08-10.md`), z `jobs.tic`
(`goodsync_jobs_2026-08-10.md`) a z rozhovoru. Aktuální stav ručních záloh kdykoli
vypíše `scripts/status.py`.

## Jak to teče

Dvě nezávislé větve, které se nesmí splést:

**1. Živá data — GoodSync, 31 jobů, přímo ze zdroje**

```
D:\Projects, Photos, Photos_XXX, Electronics, Others, Work, SVN, Git
   ├── M:\Backup\Desktop\...        WD MyCloud (síťový disk)   8 jobů
   ├── =My Passport:\...            USB disk (+ C:\...\AppData) 9 jobů
   ├── N:\...                       pracovní notebook           5 jobů
   └── D:\OneDrive\Backup\...       OneDrive (bez Git)          6 jobů
D:\Private  (jen lokální cíle — nikdy OneDrive ani notebook)
   ├── M:\Backup\Desktop\Private    WD MyCloud                  Private - Cloud
   └── =My Passport:\Private        USB disk                    Private - Disk WD
P:\Work\Stock ──> D:\Work\Backup\Stock     (z MyCloud na lokál, pull)
```

`D:\Git` (adresáře s git repozitáři) zálohují joby `Git - Cloud` (→ `M:\Backup\Desktop\Git`)
a `Git - Disk WD` (→ `=My Passport:\Git`), přidané 2026-10-16. Na OneDrive ani na
notebook job nemají.

**2. Archivy a konfigurace — do `D:\Work\Backup\`, odtud dál díky `Work` jobům**

```
zdroj ──skript / ručně──> D:\Work\Backup\...  ──jobs "Work - *"──> MyCloud, USB, Ntb, OneDrive
```

`D:\Work\Backup\` leží **uvnitř** `D:\Work`, takže ho replikují existující joby
`Work - Cloud`, `Work - Disk WD`, `Work - Ntb`, `OneDrive - Work` — pro nic tam
uloženého se nemusí zakládat nový job. Proto: **cokoli nového patří do
`D:\Work\Backup\`.** Job `Work - Cloud` vynechává `/Download - Chrome/`,
`/Download - Thunderbird/`, `/Temp/`.

Seznam jobů se generuje z `jobs.tic` (`scripts/goodsync_jobs.py`), poslední časy běhů
jsou ručně opsané z GUI v `goodsync_runs_2026-08-10.md` — automaticky je nezjistíš.

## Ruční a poloautomatické zálohy

Tohle je ta část, kterou hlídá `status.py`. Interval je naše vlastní dohoda, mění se
v `config.json`.

| id | Co | Zdroj | Metoda | Cíl v `D:\Work\Backup\` | Interval | Automatizace | Poslední (2026-08-10) |
|---|---|---|---|---|---|---|---|
| `data-others` | osobní data | `D:\Others\` | WinRAR přes `D:\Work\Skripty\backup_data.bat` | `Data\Others_YYMMDD.rar` | 90 d | poloauto — spouští se ručně | 2026-02-01 |
| `data-projects` | projekty a kód | `D:\Projects\` | tentýž .bat | `Data\Projects_YYMMDD.rar` | 90 d | poloauto — spouští se ručně | 2026-02-01 |
| `home-assistant` | HA konfigurace + historie | HA cloud (Nabu Casa) | ruční stažení `.tar` | `HomeAssistant\` | 90 d | **ručně** | 2026-02-01 (záloha z 2025-12-04) |
| `router` | konfigurace routeru a AP | Mikrotik Attic, TP-Link Archer AX10 (Obývák, Hůra), opakovače | export z webového rozhraní | `Router\<zařízení>\` | 90 d | **ručně** | 2026-06-19 (jen Mikrotik; TP-Link 2023-12-16) |
| `goodsync` | joby a nastavení GoodSync | `%APPDATA%\GoodSync` | export `.tix` z GUI, nebo `backup_configs.py` | `GoodSync\good_sync_YYMMDD.*` | 90 d | **auto** (`backup_configs.py`) | 2026-01-18 |
| `totalcmd` | konfigurace Total Commander | `%APPDATA%\GHISLER` | kopie `*.ini`, nebo `backup_configs.py` | `Total Commander\YYMMDD\` | 90 d | **auto** (`backup_configs.py`) | 2025-03-21 |
| `thunderbird` | e-maily (2 účty) | `%APPDATA%\Thunderbird\Profiles` | export do `<účet>\RRRR_MM\`; nastavení `backup_configs.py` | `Thunderbird\` | 90 d | poloauto — nastavení auto, pošta ručně | 2026-06-04 |
| `wdmycloud` | nastavení síťového disku | web WD MyCloud | export `.conf` | `WD MyCloud\` | 90 d | **ručně** | 2025-03-21 (soubor z 2024-12-10) |
| `hesla` | hesla | databáze hesel uložená v `D:\Private\` | ruční export/záloha do OneDrive Osobního trezoru | mimo `D:\Work\Backup\` — `D:\OneDrive\Osobní trezor\` | 90 d | **ručně**, mimo `status.py` | zatím nezaznamenáno |
| `todoist` | upomínky a úkoly | Todoist (web / aplikace) | ruční export | `Todoist\` | 90 d | **ručně** | zatím nezaznamenáno (doplnit při první záloze) |

Ručně navždy zůstanou `home-assistant`, `router`, `wdmycloud` a `todoist` — jsou za
webovým rozhraním. Hodnota je v tom, že je `status.py` připomene.

`hesla` je jediná položka, kterou `status.py` nehlídá, a proto není v `config.json`:
cíl je OneDrive Osobní trezor (`Osobní trezor.lnk`), zamčená složka, jejíž obsah
Windows nezpřístupní, dokud ji ručně neodemkneš. Kontrola data poslední zálohy by
tedy stejně nefungovala. Drží ji jen čtvrtletní připomínka v `rutina.md`.

Složka `D:\Work\Backup\Todoist\` zatím neexistuje; vznikne první ruční zálohou.
Do té doby ji `status.py` hlásí jako po termínu — je to správně, ne chyba.

## Cíle

| Cíl | Připojení | Kdo tam kopíruje | Poslední ověřený běh |
|---|---|---|---|
| WD MyCloud `M:` (`\\WDMYCLOUD\Marek`) | trvale, OK | GoodSync, 9 jobů (vč. `Private - Cloud`) | 2026-07-26 |
| WD MyCloud `P:` (`\\WDMYCLOUD\Public`) | trvale, OK | zdroj pro `Stock - DB` | 2026-08-09 |
| USB disk „My Passport" | ručně připojovaný | GoodSync, 10 jobů (vč. `Private - Disk WD`) | 2026-07-26 |
| OneDrive (`D:\OneDrive`) | trvale | GoodSync 6 jobů + klient OneDrive | 2026-07-26 |
| Pracovní notebook `N:` | po síti, teď odpojený | GoodSync, 5 jobů | 2026-08-09 |

## Rozhodnutí 2026-08-10

- **Retence RAR: 4 poslední + 1 na každý kalendářní rok.** Hlídá `scripts/retention.py`,
  maže se jen ručně s potvrzením.
- **`D:\School` a `D:\Led neons`**: historické věci, které se už nemění. Od 2026-10-16
  leží v `One time backup` (viz níže) a žádný GoodSync job nemají.
- **WD MyCloud se samostatně nezálohuje** — nemá to smysl, protože všechno, co na
  něm je, má další kopii jinde: na USB disku WD a na OneDrive. Výjimka je
  `D:\Private`, které jde jen na MyCloud a USB, nikdy na OneDrive (viz rozhodnutí
  2026-10-16). Samotný MyCloud má jen jeden disk a žádnou vnitřní redundanci.
- **Až bude NAS** (plánováno, termín neurčen), bude mít díky více diskům vlastní
  interní zálohu (RAID) — odolnost proti selhání disku přímo v zařízení. Pak se
  překreslí topologie, viz Otevřené otázky.
- **Automaticky denně jede z GoodSyncu jen OneDrive.** Synchronizace na `M:` (Cloud)
  trvá u některých projektů dlouho a blokovala by práci — Cloud i Ntb se
  proto spouštějí **ručně 1. v měsíci**, USB při připojení. Není to nedodělek,
  je to záměr; viz `rutina.md`.
- **Routery se doplní později** — položka `router` zůstává v `status.py`.
- **Interval je jednotně 90 dní u všech položek** kromě RAR archivů (taky 90).
  Dřív 30 / 180 / 365; sjednoceno, ať je čtyřikrát do roka jeden zálohovací den
  místo rozsypaných termínů. Čtvrtletí = **1. leden / duben / červenec / říjen**.

## One time backup — jednorázové zálohy

Složka **`One time backup`** na WD MyCloud (`M:\One time backup\`), USB disku
My Passport (`=My Passport:\One time backup\`) a OneDrive
(`D:\OneDrive\One time backup\`) obsahuje jednorázové zálohy v RAR archivech.
Neobnovují se — žádný GoodSync job, skript ani připomínka.

- `Led neons`
- `School`
- `Monika`
- `TFS Work Data`

## Rozhodnutí 2026-10-16 — `D:\Private`

- Nová složka **`D:\Private`** se soukromými věcmi. Zálohuje se **jen na lokální cíle**:
  WD MyCloud (`Private - Cloud` → `M:\Backup\Desktop\Private`) a USB disk
  (`Private - Disk WD` → `=My Passport:\Private`).
- **Nikdy na OneDrive ani na notebook** — žádný job `OneDrive - Private` / `Private - Ntb`
  nezakládat. Proto `D:\Private` taky **nepatří do `D:\Work\Backup\`** (ten replikují
  `Work` joby na OneDrive i notebook) a nebalí se do RAR v `backup_data.bat`.
- V `D:\Private` leží i **databáze hesel**. GoodSync ji tím dostane na MyCloud a USB;
  kopii mimo dům dělá dál jen ruční čtvrtletní záloha do OneDrive Osobního trezoru
  (položka `hesla`). Je to jediná věc z `D:\Private`, která smí na OneDrive — a jen
  ručně, do zamčeného trezoru.
- Periodicita jako ostatní skupiny: Cloud ručně 1. v měsíci, Disk WD při připojení USB.
- Oba joby ověřeny v `jobs.tic` 2026-10-16.

## Co je slabé místo

1. **`backup_data.bat` se pouští ručně.** Poslední běh 2026-02-01, tedy 6 měsíců.
   Automatizace přes Plánovač úloh je vědomě zamítnutá (2026-08-12); jediná pojistka
   je čtvrtletní `zalohy_ctvrtletni.bat` a připomínka v kalendáři.
2. **Nikdo nekontroluje, že GoodSync doběhl.** Cíle `M:` a USB stojí na 2026-07-26.
   Protože Cloud i Ntb zůstávají záměrně ruční, je jediná pojistka pevný termín
   1. v měsíci a připomínka v kalendáři — GoodSync sám na sebe neupozorní.
3. **Ruční položky zestárly.** TP-Link routery 2,5 roku, Total Commander 1,5 roku,
   WD MyCloud přes rok, Home Assistant 6 měsíců — všechno přes dohodnutých 90 dní.
   Total Commander a GoodSync už umí `backup_configs.py`; zbytek hlídá kalendář
   plus týdenní report ze `status.py`.
4. **~240 GB v `Data\`** — po první retenci se uvolní ~75 GB.
5. **Obnova nebyla nikdy vyzkoušena.** Záloha, ze které se nezkusilo obnovit,
   je jen doufání. Postup je v `rutina.md`, perioda ročně.
6. **`AppData` jde jen na USB** — na jediný ručně připojovaný cíl. Zatím ponecháno.

## Otevřené otázky

- Které TP-Link AP ještě v domě běží? V `Router\` jsou Zahrada, Hůra, Obývák,
  „Opakovač garáž" — část může být dávno vyřazená. Doplní se s další zálohou routerů.
- NAS s RAIDem — až bude, překreslit topologii: nahradí USB disk jako druhou kopii.
