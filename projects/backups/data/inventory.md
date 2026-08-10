# Inventura záloh

Zjištěno průzkumem stroje 2026-08-10 (`discovery_2026-08-10.md`), z `jobs.tic`
(`goodsync_jobs_2026-08-10.md`) a z rozhovoru. Aktuální stav ručních záloh kdykoli
vypíše `scripts/status.py`.

## Jak to teče

Dvě nezávislé větve, které se nesmí splést:

**1. Živá data — GoodSync, 30 jobů, přímo ze zdroje**

```
D:\Projects, Photos, Photos_XXX, Electronics, Others, Work, SVN
   ├── M:\Backup\Desktop\...        WD MyCloud (síťový disk)   7 jobů
   ├── =My Passport:\...            USB disk (+ C:\...\AppData) 8 jobů
   ├── N:\...                       pracovní notebook           5 jobů
   └── D:\OneDrive\Backup\...       OneDrive (+ Led neons, School) 8 jobů
L:\Passw  ──> D:\Work\Backup\Monika        (notebook Moniky, pull)
P:\Work\Stock ──> D:\Work\Backup\Stock     (z MyCloud na lokál, pull)
```

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

Ručně navždy zůstanou `home-assistant`, `router` a `wdmycloud` — jsou za webovým
rozhraním. Hodnota je v tom, že je `status.py` připomene.

### Neaktivní / doběhlé

| id | Co | Poslední | Poznámka |
|---|---|---|---|
| `openhab` | konfigurace OpenHAB | 2025-04-21 | **uzavřeno** — přešlo se na Home Assistant, dál se nezálohuje |
| `monika` | `L:\Passw` z notebooku Moniky | 2025-07-27 | job existuje, `L:` je odpojený |

## Cíle

| Cíl | Připojení | Kdo tam kopíruje | Poslední ověřený běh |
|---|---|---|---|
| WD MyCloud `M:` (`\\WDMYCLOUD\Marek`) | trvale, OK | GoodSync, 7 jobů | 2026-07-26 |
| WD MyCloud `P:` (`\\WDMYCLOUD\Public`) | trvale, OK | zdroj pro `Stock - DB` | 2026-08-09 |
| USB disk „My Passport" | ručně připojovaný | GoodSync, 8 jobů | 2026-07-26 |
| OneDrive (`D:\OneDrive`) | trvale | GoodSync 8 jobů + klient OneDrive | 2026-07-26 |
| Pracovní notebook `N:` | po síti, teď odpojený | GoodSync, 5 jobů | 2026-08-09 |

## Rozhodnutí 2026-08-10

- **Retence RAR: 4 poslední + 1 na každý kalendářní rok.** Hlídá `scripts/retention.py`,
  maže se jen ručně s potvrzením.
- **`D:\School` a `D:\Led neons`**: historické věci, jedna kopie v OneDrive stačí.
  Vědomě se nerozšiřuje na MyCloud ani USB — není to nedostatek.
- **Obsah WD MyCloud se nezálohuje** — druhá kopie je v OneDrive. Přehodnotí se
  s pořízením NAS s RAIDem (plánováno, termín neurčen).
- **OpenHAB uzavřen** — nahradil ho Home Assistant.
- **Automaticky denně jede z GoodSyncu jen OneDrive.** Synchronizace na `M:` (Cloud)
  trvá u některých projektů dlouho a blokovala by práci — Cloud, Ntb i Monika se
  proto spouštějí **ručně 1. v měsíci**, USB při připojení. Není to nedodělek,
  je to záměr; viz `rutina.md`.
- **Routery se doplní později** — položka `router` zůstává v `status.py`.
- **Interval je jednotně 90 dní u všech položek** kromě RAR archivů (taky 90).
  Dřív 30 / 180 / 365; sjednoceno, ať je čtyřikrát do roka jeden zálohovací den
  místo rozsypaných termínů. Čtvrtletí = **1. leden / duben / červenec / říjen**.

## Co je slabé místo

1. **`backup_data.bat` nikde není naplánovaný.** Poslední běh 2026-02-01, tedy 6 měsíců.
   Řeší `install_tasks.ps1` (čtvrtletní úloha) — po nasazení odpadá.
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
