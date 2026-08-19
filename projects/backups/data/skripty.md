# Skripty — co dělají a jak se používají

Referenční popis všech skriptů v `projects/backups/scripts/`. Co se má dít kdy je
v `rutina.md`, co se zálohuje a proč v `inventory.md`. Tady je „jak to spustit".

Všechno se spouští **z kořene repa** (`D:\Projects\AI\ai_agents_generic`), protože
cesty k venv jsou relativní k němu:

```powershell
.\.venv\Scripts\python.exe projects\backups\scripts\<skript>.py
```

## Spouštění bez příkazové řádky — `.bat` obálky

Ke každému skriptu je ve `scripts/` malá `.bat` obálka. **Dvojklik** na ni stačí —
sama najde venv, spustí se z kořene repa, na konci vypíše `[OK]` nebo `[CHYBA]`
a počká na klávesu, takže okno nezmizí.

| Dvojklik na | Spustí | Píše na disk? |
|---|---|---|
| `stav.bat` | `status.py` | ne |
| `stav_report.bat` | `status.py --md` | `data/status_*.md` |
| `retence.bat` | `retention.py` | **ne — nic nemaže** |
| `retence_smazat.bat` | `retention.py --delete` | **maže RAR archivy** (skript se ptá na potvrzení) |
| `zaloha_konfiguraci_nanecisto.bat` | `backup_configs.py --dry-run` | ne |
| `zaloha_konfiguraci.bat` | `backup_configs.py` | `D:\Work\Backup\` |
| `goodsync_joby.bat` | `goodsync_jobs.py` | `data/goodsync_jobs_*.md` |
| `pruzkum.bat` | `discover.py` | `data/discovery_*.md` |

`_run.bat` je společný spouštěč, který ty obálky volají — **nespouštěj ho přímo**.
Ověří existenci venv i skriptu, přepne se do kořene repa a předá dál návratový kód.
Nový skript = nová obálka podle vzoru: jeden `call "%~dp0_run.bat" <skript.py> <parametry>`.

Zvláštní případ zůstávají `backup_data.bat` (volá WinRAR, žádný Python) a
`zalohy_ctvrtletni.bat` (pustí celý čtvrtletní běh po sobě).

### Odkazy mimo repo — `D:\Work\Skripty\Backups\`

Obálky ve `scripts/` jdou spustit z libovolného adresáře, ale **nesmí se odtud
přesunout ani zkopírovat** — hledají kořen repa jako tři úrovně nad sebou.
Aby se nemuselo chodit do repa, je v `D:\Work\Skripty\Backups\` osm
**odkazů** stejného jména (`stav.bat`, `retence.bat`, `retence_smazat.bat`, …).
Každý jen zavolá stejnojmennou obálku v repu a vrátí její návratový kód;
žádná logika v nich není.

Cesta k repu je na jednom jediném místě — `D:\Work\Skripty\Backups\_cesta.bat`:

```bat
set "REPO=D:\Projects\AI\ai_agents_generic"
```

**Když se repo přesune, uprav tenhle jeden řádek** a všech osm odkazů zase funguje.
Dokud se neupraví, každý odkaz skončí hláškou `[CHYBA] Nenalezeno: …` s cestou
k `_cesta.bat` — nespustí se tiše nic špatného.

Ta složka **leží mimo repozitář a neverzuje se**. Je to schválně: obsahuje
absolutní cestu k tomuhle konkrétnímu stroji. Odkazy se needitují — všechny změny
chování patří do skriptů v repu. Přibude-li nový skript, přibude i nový odkaz
(vzor: `call "%~dp0_cesta.bat"`, kontrola `if not exist`, `call "%CIL%"`).

## Přehled

| Skript | Píše na disk? | Jak dlouho | Kdy se pouští |
|---|---|---|---|
| `status.py` | jen `data/status_*.md` s `--md` | vteřiny | kdykoli |
| `discover.py` | `data/discovery_*.md` | ~1 min | jednorázově, při změně stroje |
| `goodsync_jobs.py` | `data/goodsync_jobs_*.md` | vteřiny | po změně jobů v GoodSyncu |
| `backup_configs.py` | **ano — `D:\Work\Backup\`** | vteřiny | měsíčně / čtvrtletně |
| `backup_data.bat` | **ano — desítky GB** | **hodiny** | čtvrtletně, večer |
| `retention.py` | nic (bez `--delete`) | vteřiny | čtvrtletně, ručně |
| `zalohy_ctvrtletni.bat` | spouští ostatní | **hodiny** | čtvrtletně, ručně |

Nic z toho neběží samo — v Plánovači úloh Windows není naplánované nic. Vše se pouští
ručně, obvykle přes `zalohy_ctvrtletni.bat`.

Bezpečnostní zásada napříč všemi: **nic nepřepisuje ani nemaže existující zálohu.**
Když dnešní záloha už existuje, skript ji přeskočí. Jediné mazání dělá `retention.py`
a jen s `--delete` plus potvrzením z klávesnice.

---

## `status.py` — co je po termínu

Jediný skript, který budeš pouštět běžně. Pro každou položku z `config.json` najde
v její kontrolní složce nejnovější soubor odpovídající globu, spočítá jeho stáří
z času modifikace a porovná s `interval_dnu`.

Stavy: `ok` → `stárne` (nad 80 % intervalu) → `PO TERMÍNU` (nad intervalem) →
`CHYBÍ` (složka neexistuje nebo je prázdná). Výpis je seřazený od nejhoršího.

```powershell
.\.venv\Scripts\python.exe projects\backups\scripts\status.py
.\.venv\Scripts\python.exe projects\backups\scripts\status.py --md   # + report do data\
```

Jen čte. Nová položka se objeví ve výpisu hned, jak ji přidáš do `config.json` —
bez toho ji skript nikdy nepřipomene.

## `discover.py` — průzkum stroje

Vypíše disky, připojené síťové jednotky, nesystémové naplánované úlohy a známá
umístění konfigurací (GoodSync, Total Commander, Thunderbird) do
`data/discovery_RRRR-MM-DD.md`. Jen čte, podklad pro ruční aktualizaci `inventory.md`.

Pouštět po změně hardwaru nebo když nesedí, co se kam připojuje.

## `goodsync_jobs.py` — dokumentace GoodSync jobů

Rozparsuje `%APPDATA%\GoodSync\jobs.tic` (formát s délkově prefixovanými poli) a zapíše
tabulku všech jobů — odkud, kam, na který cíl — do `data/goodsync_jobs_RRRR-MM-DD.md`.

**`jobs.tic` se z tohohle projektu nikdy needituje**, jen čte; joby se spravují v GUI.
Poslední časy běhů v souboru nejsou, ty jsou pouze v GUI a přepisují se ručně do
`goodsync_runs_*.md`.

Pouštět po každé změně jobů, aby dokumentace nelhala.

## `backup_configs.py` — konfigurace do zálohy

Jediný skript, který dělá skutečnou zálohu drobných věcí:

| Co | Odkud | Kam |
|---|---|---|
| GoodSync — joby a nastavení | `%APPDATA%\GoodSync` (bez `_mirrors_`, `cookies`, `*.log`) | `GoodSync\good_sync_YYMMDD.zip` |
| Total Commander | `%APPDATA%\GHISLER\*.ini` | `Total Commander\YYMMDD\` |
| Thunderbird — **nastavení** | vybrané soubory profilu (`prefs.js`, adresář, filtry, hesla…) | `Thunderbird\nastaveni\thunderbird_<profil>_nastaveni_YYMMDD.zip` |

```powershell
.\.venv\Scripts\python.exe projects\backups\scripts\backup_configs.py --dry-run
.\.venv\Scripts\python.exe projects\backups\scripts\backup_configs.py
.\.venv\Scripts\python.exe projects\backups\scripts\backup_configs.py --thunderbird-full
```

`--thunderbird-full` přibalí i celou poštu (~19 GB) — běžně **nepoužívat**, poštu
exportuješ ručně čtvrtletně. ZIP se staví jako `*.partial` a přejmenuje se až po
dokončení, aby nešlo splést nedoběhlý archiv s hotovým. Když dnešní soubor existuje,
krok se přeskočí.

Skončí chybou, když `D:\Work\Backup` neexistuje (odpojené `D:`).

## `backup_data.bat` — RAR archivace dat

Zabalí WinRARem `D:\Others` a `D:\Projects` do
`D:\Work\Backup\Data\<Kategorie>\<Kategorie>_YYMMDD.rar`, loguje do
`Data\_log\backup_data_YYMMDD.log`.

```powershell
projects\backups\scripts\backup_data.bat
```

**Trvá hodiny a zabere desítky GB.** Pouštět večer. Kontroluje návratový kód WinRARu
(nehlásí „hotovo", když to spadlo), datum bere z PowerShellu kvůli locale a dnešní
archiv nikdy nepřepisuje — kategorii přeskočí. Novou kategorii přidáš jedním řádkem
`set "CAT[n]=Nazev=cesta"` plus zvýšením `CAT_COUNT`.

Mazání starých archivů **nedělá** — od toho je `retention.py`.

Nahrazuje starý `D:\Work\Skripty\backup_data.bat`; ten se má přestat používat.

## `retention.py` — které RAR archivy jsou nad rámec

Pravidlo z 2026-08-10, pro každou kategorii zvlášť: **4 nejnovější + 1 nejnovější
z každého kalendářního roku**, zbytek je ke smazání. Datum se bere z názvu
(`Nazev_YYMMDD.rar`), ne z času modifikace — kopírování soubor „omladí".

```powershell
.\.venv\Scripts\python.exe projects\backups\scripts\retention.py
.\.venv\Scripts\python.exe projects\backups\scripts\retention.py --out D:\Work\Backup\Data\_log\retence_report.md
.\.venv\Scripts\python.exe projects\backups\scripts\retention.py --delete
```

Bez `--delete` **nic nemaže**, jen vypíše `držet` / `SMAZAT` a kolik GB by se uvolnilo.
S `--delete` se ještě ptá — musíš napsat `smazat`. Pracuje výhradně
v `D:\Work\Backup\Data`. Automatické mazání se nikdy neplánuje.

## `zalohy_ctvrtletni.bat` — všechno najednou, ručně

Hlavní vstupní bod: jedno okno, šest kroků po sobě, všechno vidíš a kdykoli zastavíš
Ctrl+C. Spustí se dvojklikem nebo z příkazové řádky.

1. `status.py` — stav před zálohou
2. `backup_configs.py` — konfigurace
3. `backup_data.bat` — RAR archivace (**hodiny**)
4. `goodsync_jobs.py` — dokumentace jobů
5. `retention.py --out …\retence_report.md` — **jen výpis, nic nemaže**
6. `status.py --md` — stav po záloze, report do `data/`

Loguje do `D:\Work\Backup\Data\_log\zalohy_RRRR-MM-DD.log`, počítá chybné kroky
a na konci připomene ruční kroky přes webová rozhraní. Před prvním krokem ověří,
že existuje venv i `D:\Work\Backup\`.

**Automatizace přes Plánovač úloh se vědomě nepoužívá** (rozhodnuto 2026-08-12).
Ručně spouštěný dávkový soubor je vidět, dá se zastavit a nespustí hodinovou RAR
archivaci ve chvíli, kdy se to nehodí. Cenou je, že si termín musíš pohlídat sám —
od toho je připomínka v kalendáři a `status.py`.

## Co skripty neumí

Ruční navždy, protože je to za webovým rozhraním nebo fyzický úkon:
Home Assistant, routery a AP, WD MyCloud, export pošty z Thunderbirdu, Todoist,
připojení USB disku. Detaily a termíny v `rutina.md`, seznam položek v `inventory.md`.
Hodnota skriptů u nich je jen v tom, že je `status.py` připomene.
