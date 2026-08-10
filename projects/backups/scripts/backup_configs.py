"""Automatizace ručních záloh konfigurací — GoodSync, Total Commander, Thunderbird.

Tyhle tři položky byly čistě ruční, přitom je to jen kopírování lokálních souborů.
Skript je slije do `D:\\Work\\Backup\\...` pod datované jméno, odkud si je vezme
GoodSync jako všechno ostatní. Nic nepřepisuje — každý běh je nový soubor.

Co skript NEUMÍ a zůstává ruční: Home Assistant, routery, WD MyCloud.
Ty vyžadují stažení z webového rozhraní. Připomíná je `scripts/status.py`.

Spuštění:
  .\\.venv\\Scripts\\python.exe projects/backups/scripts/backup_configs.py --dry-run
  .\\.venv\\Scripts\\python.exe projects/backups/scripts/backup_configs.py
  ... --thunderbird-full   přibalí i celý profil (~19 GB, trvá dlouho)
"""

from __future__ import annotations

import json
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
CONFIG = json.loads((PROJECT_DIR / "config.json").read_text(encoding="utf-8"))
STAMP = date.today().strftime("%y%m%d")
BACKUP_ROOT = Path(CONFIG["backup_root"])
SOURCES = CONFIG["zdroje_konfiguraci"]

# GoodSync: joby a nastavení. Logy a zrcadla do zálohy nepatří — jsou velké a dočasné.
GOODSYNC_SKIP_DIRS = {"_mirrors_", "cookies"}
GOODSYNC_SKIP_SUFFIX = {".log"}

# Thunderbird: co z profilu je vlastní nastavení. Pošta samotná je v ImapMail/Mail
# a ta jde jen s --thunderbird-full.
TB_SETTINGS = (
    "prefs.js",
    "abook.sqlite",
    "history.sqlite",
    "msgFilterRules.dat",
    "logins.json",
    "key4.db",
    "signons.sqlite",
    "extensions.json",
    "virtualFolders.dat",
)

dry_run = "--dry-run" in sys.argv


def log(message: str) -> None:
    print(("[dry-run] " if dry_run else "") + message)


def zip_files(target: Path, files: list[tuple[Path, str]]) -> None:
    """Zabalí (zdroj, jméno v archivu) do ZIPu. Cíl nesmí existovat."""
    if target.exists():
        log(f"přeskočeno, dnešní záloha už existuje: {target}")
        return
    total_mb = sum(src.stat().st_size for src, _ in files) / 1024 / 1024
    log(f"{target}  ({len(files)} souborů, {total_mb:.1f} MB nekomprimovaně)")
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".partial")
    with zipfile.ZipFile(partial, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in files:
            zf.write(src, arcname)
    partial.rename(target)  # ať se nedá splést nedoběhlý archiv s hotovým


def walk(root: Path, skip_dirs: set[str] = frozenset(), skip_suffix: set[str] = frozenset()):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in skip_dirs for part in rel.parts):
            continue
        if path.suffix.lower() in skip_suffix:
            continue
        yield path, str(rel)


def backup_goodsync() -> None:
    src = Path(SOURCES["goodsync"])
    if not src.exists():
        log(f"CHYBÍ zdroj GoodSync: {src}")
        return
    files = list(walk(src, GOODSYNC_SKIP_DIRS, GOODSYNC_SKIP_SUFFIX))
    zip_files(BACKUP_ROOT / "GoodSync" / f"good_sync_{STAMP}.zip", files)


def backup_totalcmd() -> None:
    """Total Commander — dvě ini, kopie do datované podsložky (bez zipu, jsou drobné)."""
    src = Path(SOURCES["totalcmd"])
    if not src.exists():
        log(f"CHYBÍ zdroj Total Commander: {src}")
        return
    target_dir = BACKUP_ROOT / "Total Commander" / STAMP
    inis = sorted(src.glob("*.ini"))
    if not inis:
        log(f"v {src} nejsou žádné .ini")
        return
    log(f"{target_dir}\\  ({len(inis)} × .ini)")
    if dry_run:
        return
    target_dir.mkdir(parents=True, exist_ok=True)
    for ini in inis:
        shutil.copy2(ini, target_dir / ini.name)


def backup_thunderbird(full: bool) -> None:
    root = Path(SOURCES["thunderbird_profily"])
    if not root.exists():
        log(f"CHYBÍ zdroj Thunderbird: {root}")
        return
    profiles = [p for p in root.iterdir() if p.is_dir()]
    if not profiles:
        log(f"v {root} není žádný profil")
        return
    for profile in profiles:
        if full:
            files = list(walk(profile))
            name = f"thunderbird_{profile.name}_plny_{STAMP}.zip"
        else:
            files = [
                (profile / n, n) for n in TB_SETTINGS if (profile / n).is_file()
            ]
            name = f"thunderbird_{profile.name}_nastaveni_{STAMP}.zip"
        if not files:
            log(f"profil {profile.name}: nic k zabalení")
            continue
        zip_files(BACKUP_ROOT / "Thunderbird" / "nastaveni" / name, files)


def main() -> None:
    if not BACKUP_ROOT.exists():
        print(f"Cíl {BACKUP_ROOT} neexistuje — je připojený disk D:?")
        sys.exit(1)
    full = "--thunderbird-full" in sys.argv
    backup_goodsync()
    backup_totalcmd()
    backup_thunderbird(full)
    if not full:
        print("\nPošta samotná nezazálohována — to dělá `--thunderbird-full` (~19 GB).")
    print("Ručně zbývá: Home Assistant, routery, WD MyCloud. Viz data/inventory.md.")


if __name__ == "__main__":
    main()
