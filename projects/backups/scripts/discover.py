"""Průzkum stroje — co tu je za disky, naplánované úlohy a zálohovací nástroje.

Jen čte. Nic nemaže, nic nekopíruje. Výstup je markdown report v temp/
s datem v názvu, který slouží jako podklad pro data/inventory.md.

Spuštění:  .\\.venv\\Scripts\\python.exe projects/backups/scripts/discover.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.lib.repo import dated, temp_dir  # noqa: E402

PROJECT = Path(__file__).resolve().parents[1].name

# Místa, kde obvykle leží konfigurace nástrojů, které uživatel zálohuje ručně.
CONFIG_HINTS: dict[str, list[str]] = {
    "GoodSync": [
        r"%USERPROFILE%\AppData\Roaming\GoodSync",
        r"%LOCALAPPDATA%\GoodSync",
        r"%PROGRAMDATA%\Siber Systems\GoodSync",
    ],
    "Total Commander": [
        r"%APPDATA%\GHISLER",
        r"C:\totalcmd",
        r"C:\Program Files\totalcmd",
    ],
    "Thunderbird": [
        r"%APPDATA%\Thunderbird\Profiles",
    ],
    "Home Assistant (lokální kopie záloh)": [
        r"%USERPROFILE%\Downloads",
        r"%USERPROFILE%\Documents\HomeAssistant",
    ],
}


def ps(command: str) -> str:
    """Spustí PowerShell příkaz a vrátí stdout (prázdný string při chybě)."""
    try:
        out = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return out.stdout.strip()
    except Exception as exc:  # noqa: BLE001 - report, nezastavuj průzkum
        return f"(nezjištěno: {exc})"


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip() or '_nic nenalezeno_'}\n\n"


def drives() -> str:
    out = ps(
        "Get-Volume | Where-Object DriveLetter | "
        "Select-Object DriveLetter,FileSystemLabel,DriveType,"
        "@{n='SizeGB';e={[math]::Round($_.Size/1GB,1)}},"
        "@{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}} | "
        "Format-Table -AutoSize | Out-String -Width 200"
    )
    return f"```\n{out}\n```"


def network_shares() -> str:
    mapped = ps("net use | Out-String -Width 200")
    return f"Připojené síťové jednotky:\n\n```\n{mapped}\n```"


def scheduled_tasks() -> str:
    out = ps(
        "Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\\Microsoft\\*' } | "
        "ForEach-Object { $i = $_ | Get-ScheduledTaskInfo; "
        "'{0,-45} {1,-9} {2}' -f $_.TaskName, $_.State, $i.LastRunTime } | "
        "Out-String -Width 200"
    )
    return (
        "Naplánované úlohy mimo systémové (tady se pozná, co už běží samo):\n\n"
        f"```\n{out}\n```"
    )


def config_locations() -> str:
    rows = ["| Nástroj | Cesta | Existuje |", "|---|---|---|"]
    for tool, candidates in CONFIG_HINTS.items():
        for raw in candidates:
            expanded = Path(os.path.expandvars(raw))
            exists = "ano" if expanded.exists() else "ne"
            rows.append(f"| {tool} | `{expanded}` | {exists} |")
    return "\n".join(rows)


def existing_zip_scripts() -> str:
    """Hledá stávající zálohovací skripty uživatele (ty, co dělají zipy)."""
    roots = [
        Path(os.path.expandvars(r"%USERPROFILE%")),
        Path("C:/Scripts"),
        Path("D:/Scripts"),
    ]
    patterns = ("*.bat", "*.cmd", "*.ps1")
    keywords = ("backup", "zaloh", "záloh", "zip", "goodsync")
    hits: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        for pattern in patterns:
            for path in root.glob(f"*/{pattern}"):
                if any(k in path.name.lower() for k in keywords):
                    hits.append(f"- `{path}`")
        for pattern in patterns:
            for path in root.glob(pattern):
                if any(k in path.name.lower() for k in keywords):
                    hits.append(f"- `{path}`")
    return "\n".join(sorted(set(hits)))


def main() -> None:
    report = f"# Průzkum stroje — {dated('', '').strip('_')}\n\n"
    report += "> Generuje `scripts/discover.py`. Podklad pro `data/inventory.md`.\n\n"
    report += section("Disky", drives())
    report += section("Síťová úložiště", network_shares())
    report += section("Naplánované úlohy", scheduled_tasks())
    report += section("Kde leží konfigurace zálohovaných nástrojů", config_locations())
    report += section("Nalezené existující zálohovací skripty", existing_zip_scripts())

    target = temp_dir(PROJECT) / dated("discovery", ".md")
    target.write_text(report, encoding="utf-8")
    print(f"Zapsáno: {target}")


if __name__ == "__main__":
    main()
