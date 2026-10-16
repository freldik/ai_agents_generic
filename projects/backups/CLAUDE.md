# Projekt: backups

## Účel

Správa všech záloh na tomto počítači — zdokumentovat, co se zálohuje kam a jak často,
hlásit zastaralé zálohy a postupně převádět ruční kroky na skripty.
Výchozí stav (2026-08-10): jedna položka poloautomatická, sedm ručních.

Celý řetězec, rozhodnutí a slabá místa jsou v **`data/inventory.md`** — čti ho první.
Co běží samo a co musí uživatel ručně, je v **`data/rutina.md`**.
Podrobný popis skriptů — co dělají, jaké mají přepínače a jak se spouštějí — je
v **`data/skripty.md`**.

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `data/inventory.md` | inventura záloh: co, odkud, kam, jak často, slabá místa | ručně, podle průzkumu a rozhovoru |
| `data/rutina.md` | naplánované úlohy, návrh periodicity GoodSyncu, ruční připomínky | ručně |
| `config.json` | strojová verze inventury — cesty, globy, intervaly | ručně; `id` musí souhlasit s `inventory.md` |
| `temp/discovery_*.md` | průzkum stroje — disky, síťové jednotky, úlohy | generuje `discover.py` |
| `temp/goodsync_jobs_*.md` | seznam všech GoodSync jobů: odkud, kam | generuje `goodsync_jobs.py` z `jobs.tic` |
| `data/goodsync_runs_*.md` | poslední časy běhů jobů | **ručně** opsáno z GUI — jinak se nezjistí |
| `temp/status_*.md` | snapshot stavu záloh k datu | generuje `status.py --md` |

Zálohy samotné žijí v `D:\Work\Backup\` — **mimo tento repozitář** a tenhle projekt
je nikdy nemaže ani nepřepisuje. V repu je jen dokumentace a skripty.

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/discover.py` | prohledá stroj (disky, síťové jednotky, naplánované úlohy, umístění konfigurací) a zapíše report. Jen čte. |
| `scripts/goodsync_jobs.py` | rozparsuje `%APPDATA%\GoodSync\jobs.tic` a vypíše všechny joby (2026-10-16: 31) jako tabulku. Jen čte. |
| `scripts/status.py` | pro každou položku najde nejnovější zálohu a porovná s intervalem; hlásí `PO TERMÍNU` / `stárne` / `ok`. `--md` uloží report. |
| `scripts/backup_configs.py` | zazálohuje konfigurace GoodSync, Total Commander a nastavení Thunderbirdu do `D:\Work\Backup\`. `--dry-run` nejdřív. |
| `scripts/backup_data.bat` | WinRAR archivace `D:\Others` a `D:\Projects` do `D:\Work\Backup\Data\<Kategorie>\`. Nahrazuje starý `D:\Work\Skripty\backup_data.bat`. |
| `scripts/retention.py` | vypíše RAR archivy nad rámec 4+1/rok. **Bez `--delete` nemaže**, s ním se ptá na potvrzení. |
| `scripts/_run.bat` + `stav.bat`, `retence.bat`, `retence_smazat.bat`, … | `.bat` obálky nad python skripty — dvojklik místo příkazové řádky. Seznam v `data/skripty.md`. Nový python skript = i nová obálka. |
| `scripts/zalohy_ctvrtletni.bat` | ruční čtvrtletní běh — pustí po sobě status, konfigurace, RAR, dokumentaci jobů, retenci (jen výpis) a závěrečný status. Tudy jde všechno. |

Spouštění z kořene repa:
`.\.venv\Scripts\python.exe projects/backups/scripts/status.py`

Bez příkazové řádky: dvojklik na `.bat` obálku ve `scripts/`, nebo na stejnojmenný
odkaz v `D:\Work\Skripty\Backups\` (mimo repo, neverzuje se — drží jen absolutní
cestu k repu v `_cesta.bat`). Podrobnosti v `data/skripty.md`.

## Pravidla specifická pro tento projekt

- **Nová záloha patří do `D:\Work\Backup\`.** Ta složka leží uvnitř `D:\Work`, které
  už replikují joby `Work - Cloud` / `Work - Disk WD` / `Work - Ntb` / `OneDrive - Work`
  na všechny čtyři cíle. Nezakládej kvůli nové záloze nový GoodSync job a nevymýšlej
  nové cíle. **Pozor:** živá data (`D:\Projects`, `D:\Photos`, …) jdou do GoodSyncu
  přímo ze zdroje, ne přes `Backup\` — to jsou dvě různé větve, viz `data/inventory.md`.
- **`D:\Private` jen na lokální cíle** (rozhodnuto 2026-10-16): joby `Private - Cloud`
  (MyCloud) a `Private - Disk WD` (USB). Nikdy nenavrhuj OneDrive ani notebook, nekopíruj
  nic z `D:\Private` do `D:\Work\Backup\` a nebal ho do RAR. Databáze hesel v něm jde
  na OneDrive jen ručně do Osobního trezoru (položka `hesla`).
- **Nikdy nemaž ani nepřepisuj existující zálohu.** Každý běh vytvoří nový datovaný
  soubor. Když už dnešní záloha existuje, skript ji přeskočí, nepřepíše.
  Retence RAR archivů je **4 poslední + 1 na kalendářní rok** (`retention.py`),
  ale mazání spouští vždy uživatel. Automatické mazání nikdy nenavrhuj ani neplánuj.
- **Datum v názvu záloh je `YYMMDD`**, ne `YYYY-MM-DD` — drží to konvenci
  existujícího `backup_data.bat` a starých archivů. Uvnitř repa platí `YYYY-MM-DD`.
- **Nic neběží přes Plánovač úloh Windows.** Rozhodnuto 2026-08-12: zálohuje se
  ručně čtvrtletním `zalohy_ctvrtletni.bat`, ať je běh vidět a dá se zastavit.
  Nenavrhuj naplánované úlohy ani je nezakládej.
- **Nový skript je nejdřív `--dry-run`.** Cílem je disk s desítkami GB dat.
- **`jobs.tic` se nikdy needituje skriptem.** Joby se spravují v GUI GoodSyncu;
  odsud se z něj jen čte. Rozbitý `jobs.tic` znamená rozbité všechny zálohy.
- **Nespouštěj destruktivní operace na `M:`, `P:` ani `E:`.** Síťový disk a USB jsou
  poslední instance záloh; tento projekt na ně jen čte.
- Když přidáš položku, přidej ji do `config.json` **i** do `data/inventory.md`.
  Bez záznamu v `config.json` ji `status.py` nikdy nepřipomene.
- Ruční kroky, které nejde zautomatizovat (Home Assistant, routery, WD MyCloud —
  všechno přes webové rozhraní), zůstávají ruční. Neslibuj u nich automatizaci;
  hodnota je v tom, že je `status.py` připomene.

- **Co se vědomě nezálohuje** (rozhodnuto 2026-08-10, neotevírat znovu):
  složka `One time backup` na MyCloud, USB i OneDrive obsahuje jen jednorázové
  RAR archivy (`Led neons`, `School`, `Monika`, `TFS Work Data`) — žádný job, nic
  se do ní nepřidává ani nemaže; WD MyCloud se samostatně nezálohuje — jeho obsah má kopii na USB disku WD a na OneDrive
  (kromě `D:\Private`: jen MyCloud + USB). Interní redundanci přinese až NAS s více disky.

## Otevřené otázky

- Přenastavení GoodSync jobů podle `data/rutina.md` zatím **neproběhlo**.
- Starý `D:\Work\Skripty\backup_data.bat` se má nahradit tím ze `scripts/` — taky ne.
- Zálohovat i notebooky (`FRELICHOVA-NTB`, `FRELICH-NTB`)?
- Zbytek otevřených otázek k jednotlivým položkám je v `data/inventory.md`.
