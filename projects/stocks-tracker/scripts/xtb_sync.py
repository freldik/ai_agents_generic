"""Aktualizuje sloupce Investovano a Hodnota v sporeni.xlsx podle exportů z brokerů.

Exporty se hledají ve stromu:

    <kořen>/<Vlastnik>/<Broker>/<MENA>_....xlsx

např. `D:\\Work\\Sporeni\\Test\\Marek\\XTB\\USD_51959804_2006-01-01_2026-08-13.xlsx`.
V každé složce brokera smí být pro jednu měnu **právě jeden** soubor — konkrétní název
se proto nikde nezadává. Měna se pozná z předpony názvu (`USD_`, `EUR_`, `CZK_`).

Do sešitu se zapisují jen sloupce Investovano <MENA> a Hodnota <MENA> na řádcích akcií.
Nic jiného se nemění. Sešit má grafy, tabulky a webextension, které by openpyxl při
uložení poškodil, takže se hodnoty zapisují přímo do XML uvnitř .xlsx.

Spuštění z kořene repa:
    .\\.venv\\Scripts\\python.exe projects/stocks-tracker/scripts/xtb_sync.py --dry-run
    .\\.venv\\Scripts\\python.exe projects/stocks-tracker/scripts/xtb_sync.py --write
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.lib.repo import data_dir, dated  # noqa: E402

PROJECT = "stocks-tracker"

ROOT = Path(r"D:\Work\Sporeni\Test")  # kořen se složkami vlastníků
SPORENI = ROOT / "sporeni.xlsx"

CURRENCIES = ("USD", "EUR", "CZK")

# Sešit má jeden společný list "Akcie" se sloupci Vlastnik a Broker. Dřív byl list
# na každého vlastníka zvlášť ("Akcie - XTB (Moje)"), a kdyby se k tomu někdy vrátil,
# skript takový list pozná podle názvu.
SHEET_PATTERN = re.compile(r"^Akcie - (?P<broker>.+?) \((?P<owner>.+?)\)$")
OWNER_ALIASES = {"moje": "marek"}

# Názvy, které se mezi sešitem a exportem liší víc, než srovná normalizace.
ALIASES = {
    "treasurybondib01usd": "treasurybond01y",
    "arcelormital": "arcelormittal",
    "baesystems": "bae",
    "mcdonald": "mcdonalds",
    "coreeurostoxx50": "eurostoxx50",
}


def norm(name: str) -> str:
    """Porovnávací tvar názvu: malá písmena, jen alfanumerické znaky."""
    key = re.sub(r"[^a-z0-9]", "", str(name).lower())
    return ALIASES.get(key, key)


def norm_owner(name: str) -> str:
    key = re.sub(r"[^a-z0-9]", "", str(name).lower())
    return OWNER_ALIASES.get(key, key)


# ---------------------------------------------------------------- exporty


def find_exports(root: Path) -> dict[tuple[str, str], dict[str, Path]]:
    """Projde strom vlastník/broker a vrátí {(vlastnik, broker): {mena: soubor}}.

    Hlídá, že pro jednu měnu je ve složce právě jeden soubor — jinak by nebylo jasné,
    který se má použít.
    """
    if not root.is_dir():
        raise SystemExit(f"Kořen exportů neexistuje: {root}")

    found: dict[tuple[str, str], dict[str, Path]] = {}
    problems: list[str] = []

    for owner_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for broker_dir in sorted(p for p in owner_dir.iterdir() if p.is_dir()):
            files = [
                f
                for f in sorted(broker_dir.glob("*.xlsx"))
                if not f.name.startswith("~$") and not f.name.endswith(".bak.xlsx")
            ]
            if not files:
                problems.append(f"{owner_dir.name}/{broker_dir.name}: složka je prázdná")
                continue

            by_currency: dict[str, list[Path]] = {}
            for f in files:
                currency = f.name.split("_", 1)[0].upper()
                if currency not in CURRENCIES:
                    problems.append(
                        f"{owner_dir.name}/{broker_dir.name}/{f.name}: "
                        f"název nezačíná měnou ({', '.join(CURRENCIES)})"
                    )
                    continue
                by_currency.setdefault(currency, []).append(f)

            for currency, group in by_currency.items():
                if len(group) > 1:
                    names = ", ".join(f.name for f in group)
                    problems.append(
                        f"{owner_dir.name}/{broker_dir.name}: pro {currency} je souborů "
                        f"{len(group)} ({names}) — nech ve složce jen ten aktuální"
                    )

            usable = {c: g[0] for c, g in by_currency.items() if len(g) == 1}
            if usable:
                found[(owner_dir.name, broker_dir.name)] = usable

    if problems:
        raise SystemExit("Exporty nejsou v pořádku:\n  " + "\n  ".join(problems))
    if not found:
        raise SystemExit(f"Pod {root} nejsou žádné exporty ve tvaru <Vlastnik>/<Broker>/<MENA>_*.xlsx")
    return found


def read_export(path: Path) -> dict[str, dict]:
    """Souhrnné řádky exportu (ty s vyplněnou kategorií), klíč = normalizovaný název.

    Investováno = Value - Net Profit, tj. hodnota bez zisku. Sedí na Volume * Open price.
    """
    # Bez read_only: export nemá v XML rozsah listu a v režimu jen pro čtení
    # by openpyxl viděl prázdný list.
    wb = openpyxl.load_workbook(path, data_only=True)
    if "Open Positions" not in wb.sheetnames:
        raise SystemExit(f"{path.name}: chybí list 'Open Positions' — je to export otevřených pozic?")
    ws = wb["Open Positions"]

    out: dict[str, dict] = {}
    for row in ws.iter_rows(min_row=10, max_col=14, values_only=True):
        name, ticker, category = row[1], row[2], row[3]
        value, net = row[6], row[13]
        if not category or not name:  # prázdná kategorie = dílčí obchod, ne souhrn
            continue
        key = norm(name)
        if key in out:
            raise SystemExit(f"{path.name}: dva souhrnné řádky pro '{name}' — mapování by bylo nejisté.")
        out[key] = {
            "name": name,
            "ticker": ticker or "",
            "invested": (value or 0) - (net or 0),
            "value": value or 0,
        }
    wb.close()
    return out


# ---------------------------------------------------------------- sešit


class SheetLayout:
    """Kde na listu leží data — sloupce se hledají podle hlaviček, ne natvrdo.

    Listy jednotlivých vlastníků mají různé rozložení: Markův má navíc Vlastnik
    a Broker a začíná Investovanem v E, ostatní v C.
    """

    def __init__(self, ws) -> None:
        self.title = ws.title
        self.headers = {
            str(c.value).strip(): c.column_letter for c in ws[1] if c.value is not None
        }
        self.first_row, self.last_row = self._data_rows(ws)

        missing = [
            f"{kind} {ccy}"
            for kind in ("Investovano", "Hodnota")
            for ccy in CURRENCIES
            if f"{kind} {ccy}" not in self.headers
        ]
        if "Akcie" not in self.headers:
            missing.insert(0, "Akcie")
        if missing:
            raise SystemExit(f"List '{ws.title}': chybí sloupce {', '.join(missing)}")

    @staticmethod
    def _data_rows(ws) -> tuple[int, int]:
        """Rozsah řádků z tabulky, která začíná v A1 — ne z max_row (pod tabulkou jsou součty)."""
        for table in ws.tables.values():
            start, end = table.ref.split(":")
            if start.rstrip("0123456789") == "A" and start.endswith("1"):
                return 2, int(re.sub(r"[A-Z]", "", end))
        raise SystemExit(f"List '{ws.title}': nenašel jsem tabulku začínající v A1")

    def col(self, header: str) -> str:
        return self.headers[header]

    def cell(self, header: str, row: int) -> str:
        return f"{self.col(header)}{row}"


def find_sheets(wb) -> tuple[list[str], dict[tuple[str, str], str]]:
    """Rozdělí listy na společné (mají sloupce Vlastnik + Broker) a pojmenované.

    Vrací (společné listy, {(vlastnik, broker): pojmenovaný list}).
    """
    shared, named = [], {}
    for title in wb.sheetnames:
        ws = wb[title]
        headers = {str(c.value).strip() for c in ws[1] if c.value is not None}
        if not {"Akcie", "Investovano USD", "Hodnota USD"} <= headers:
            continue
        if {"Vlastnik", "Broker"} <= headers:
            shared.append(title)
        match = SHEET_PATTERN.match(title)
        if match:
            named[(norm_owner(match["owner"]), match["broker"].strip().lower())] = title
    return shared, named


def resolve_sheet(owner: str, broker: str, shared: list[str], named: dict) -> str:
    """Kam patří řádky daného vlastníka a brokera."""
    key = (norm_owner(owner), broker.strip().lower())
    if key in named:
        return named[key]
    if len(shared) == 1:
        return shared[0]
    if not shared:
        raise SystemExit(
            f"Pro {owner}/{broker} není v sešitu list. Čekám buď společný list se sloupci "
            f"Vlastnik a Broker, nebo list 'Akcie - {broker} ({owner})'."
        )
    raise SystemExit(
        f"Společných listů se sloupci Vlastnik a Broker je víc ({', '.join(shared)}) — "
        f"nevím, kam {owner}/{broker} patří."
    )


def plan(sporeni: Path, root: Path) -> tuple[dict[str, dict[str, float]], list[dict]]:
    """Vrátí (buňky k zápisu podle listů, přehled po vlastníkovi a brokerovi)."""
    exports = find_exports(root)
    wb = openpyxl.load_workbook(sporeni)
    shared, named = find_sheets(wb)

    cells: dict[str, dict[str, float]] = {}
    blocks: list[dict] = []

    for (owner, broker), files in sorted(exports.items()):
        title = resolve_sheet(owner, broker, shared, named)
        ws = wb[title]
        layout = SheetLayout(ws)
        positions = {ccy: read_export(path) for ccy, path in files.items()}

        rows, unmatched, used = [], [], {ccy: set() for ccy in CURRENCIES}

        for row in range(layout.first_row, layout.last_row + 1):
            name = ws[layout.cell("Akcie", row)].value
            if not name:
                continue
            if "Vlastnik" in layout.headers:
                value = ws[layout.cell("Vlastnik", row)].value
                if value and norm_owner(value) != norm_owner(owner):
                    continue
            if "Broker" in layout.headers:
                value = ws[layout.cell("Broker", row)].value
                if value and str(value).strip().lower() != broker.strip().lower():
                    continue

            entry = {"row": row, "name": str(name), "ticker": "", "values": {}}
            matched_any = False

            for ccy in CURRENCIES:
                pos = positions.get(ccy, {}).get(norm(name))
                if pos is None:
                    new_inv = new_val = 0
                else:
                    matched_any = True
                    used[ccy].add(norm(name))
                    new_inv, new_val = round(pos["invested"]), round(pos["value"])
                    entry["ticker"] = entry["ticker"] or pos["ticker"]

                inv_ref = layout.cell(f"Investovano {ccy}", row)
                val_ref = layout.cell(f"Hodnota {ccy}", row)
                entry["values"][ccy] = {
                    "old_inv": ws[inv_ref].value or 0,
                    "new_inv": new_inv,
                    "old_val": ws[val_ref].value or 0,
                    "new_val": new_val,
                }
                cells.setdefault(title, {})[inv_ref] = new_inv
                cells.setdefault(title, {})[val_ref] = new_val

            entry["changed"] = any(
                v["old_inv"] != v["new_inv"] or v["old_val"] != v["new_val"]
                for v in entry["values"].values()
            )
            if not matched_any:
                unmatched.append(entry)
            rows.append(entry)

        leftover = {
            ccy: [positions[ccy][k]["name"] for k in positions[ccy] if k not in used[ccy]]
            for ccy in positions
        }

        blocks.append(
            {
                "owner": owner,
                "broker": broker,
                "sheet": title,
                "files": files,
                "rows": rows,
                "unmatched": unmatched,
                "leftover": {c: v for c, v in leftover.items() if v},
            }
        )

    return cells, blocks


# ---------------------------------------------------------------- report


def _pair(old, new) -> str:
    if old == new:
        return f"{old}"
    return f"{old} → **{new}**"


def markdown_report(blocks: list[dict], sporeni: Path, root: Path, written: bool) -> str:
    total_changed = sum(len([r for r in b["rows"] if r["changed"]]) for b in blocks)
    lines = [
        f"# Aktualizace {sporeni.name}",
        "",
        f"- Spuštěno: {datetime.now():%Y-%m-%d %H:%M}",
        f"- Kořen exportů: `{root}`",
        f"- Režim: {'**zapsáno do sešitu**' if written else 'jen výpis, nic se nezapsalo'}",
        f"- Změněných řádků celkem: **{total_changed}**",
        "",
        "Zapisují se jen sloupce Investovano a Hodnota. Měna, pro kterou ve složce brokera",
        "není export, se nastavuje na 0 — tedy „v této měně nic nedržím“.",
    ]

    for block in blocks:
        changed = [r for r in block["rows"] if r["changed"]]
        lines += [
            "",
            f"## {block['owner']} — {block['broker']}",
            "",
        ]
        if not block["rows"]:
            lines += [
                f"**Export existuje, ale na listě `{block['sheet']}` nemá "
                f"{block['owner']} / {block['broker']} jediný řádek — nezapsalo se nic.**",
                "",
                "Přidej řádky s těmito hodnotami ve sloupcích `Vlastnik` a `Broker`, "
                "jinak se tyhle pozice do přehledu nikdy nedostanou.",
                "",
            ]
        lines += [
            f"- List: `{block['sheet']}`",
            f"- Změněných řádků: **{len(changed)}** z {len(block['rows'])}",
            "- Exporty: "
            + ", ".join(f"{ccy} `{p.name}`" for ccy, p in sorted(block["files"].items()))
            + (
                ""
                if len(block["files"]) == len(CURRENCIES)
                else "  (chybějící měny: "
                + ", ".join(c for c in CURRENCIES if c not in block["files"])
                + " → 0)"
            ),
            "",
            "| Ř. | Akcie | Ticker | Inv. USD | Inv. EUR | Inv. CZK | Hodn. USD | Hodn. EUR | Hodn. CZK |",
            "|---:|---|---|---:|---:|---:|---:|---:|---:|",
        ]
        for r in block["rows"]:
            v = r["values"]
            mark = "" if r["changed"] else " _(beze změny)_"
            lines.append(
                f"| {r['row']} | {r['name']}{mark} | {r['ticker'] or '—'} | "
                + " | ".join(_pair(v[c]["old_inv"], v[c]["new_inv"]) for c in CURRENCIES)
                + " | "
                + " | ".join(_pair(v[c]["old_val"], v[c]["new_val"]) for c in CURRENCIES)
                + " |"
            )

        sums = {
            c: {
                k: sum(r["values"][c][k] for r in block["rows"])
                for k in ("old_inv", "new_inv", "old_val", "new_val")
            }
            for c in CURRENCIES
        }
        lines.append(
            "| | **Celkem** | | "
            + " | ".join(_pair(sums[c]["old_inv"], sums[c]["new_inv"]) for c in CURRENCIES)
            + " | "
            + " | ".join(_pair(sums[c]["old_val"], sums[c]["new_val"]) for c in CURRENCIES)
            + " |"
        )

        if block["unmatched"]:
            lines += ["", "**Bez otevřené pozice v žádném exportu** (zapsána 0):", ""]
            lines += [f"- ř. {r['row']} — {r['name']}" for r in block["unmatched"]]
        if block["leftover"]:
            lines += ["", "**POZOR: pozice z exportu, které nemají řádek v sešitu**", ""]
            for ccy, names in sorted(block["leftover"].items()):
                lines += [f"- {ccy}: {n}" for n in names]

    return "\n".join(lines) + "\n"


def console_summary(blocks: list[dict]) -> str:
    lines = []
    for block in blocks:
        changed = [r for r in block["rows"] if r["changed"]]
        lines.append(f"\n{block['owner']} / {block['broker']}  →  list '{block['sheet']}'")
        lines.append(
            f"  exporty: {', '.join(sorted(block['files'])) or 'žádné'}"
            f"   změněných řádků: {len(changed)} z {len(block['rows'])}"
        )
        if not block["rows"]:
            lines.append(
                f"  !! na listu není jediný řádek s Vlastnik={block['owner']} "
                f"a Broker={block['broker']} — nezapsalo se nic"
            )
        for r in changed:
            parts = []
            for ccy in CURRENCIES:
                v = r["values"][ccy]
                if v["old_inv"] != v["new_inv"] or v["old_val"] != v["new_val"]:
                    parts.append(
                        f"{ccy} inv {v['old_inv']}->{v['new_inv']}, hodn {v['old_val']}->{v['new_val']}"
                    )
            lines.append(f"    ř.{r['row']:>3} {r['name']:<28} " + "; ".join(parts))
        if block["leftover"]:
            for ccy, names in sorted(block["leftover"].items()):
                lines.append(f"  ! {ccy}: v exportu, ale bez řádku v sešitu: {', '.join(names)}")
    return "\n".join(lines)


# ---------------------------------------------------------------- zápis


def sheet_paths(path: Path) -> dict[str, str]:
    """{název listu: cesta k jeho XML v zipu}."""
    with zipfile.ZipFile(path) as z:
        wb = z.read("xl/workbook.xml").decode("utf-8")
        rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    out = {}
    for name, rid in re.findall(r'<sheet name="([^"]+)"[^>]*r:id="([^"]+)"', wb):
        target = re.search(rf'Id="{rid}"[^>]*Target="([^"]+)"', rels)
        if target:
            out[name.replace("&amp;", "&")] = "xl/" + target.group(1).lstrip("/")
    return out


def write_cells(path: Path, per_sheet: dict[str, dict[str, float]]) -> Path:
    """Přepíše hodnoty daných buněk přímo v XML; zbytek sešitu zůstane beze změny."""
    lock = path.with_name("~$" + path.name)
    if lock.exists():
        raise SystemExit(
            f"Sešit je otevřený v Excelu ({lock.name}). Zavři ho — jinak by Excel při "
            f"uložení přepsal, co skript zapíše."
        )
    backup = path.with_suffix(".bak.xlsx")
    shutil.copy2(path, backup)

    with zipfile.ZipFile(path) as zin:
        items = {n: zin.read(n) for n in zin.namelist()}
        infos = {i.filename: i for i in zin.infolist()}

    paths = sheet_paths(path)
    for title, cells in per_sheet.items():
        xml_name = paths.get(title)
        if xml_name is None:
            raise SystemExit(f"List '{title}' nemá v sešitu XML — struktura se změnila.")
        xml = items[xml_name].decode("utf-8")
        for ref, value in cells.items():
            pattern = re.compile(rf'<c r="{ref}"([^>]*?)(/>|>.*?</c>)', re.DOTALL)
            match = pattern.search(xml)
            if not match:
                raise SystemExit(f"Buňka {ref} na listu '{title}' v XML nenalezena.")
            attrs = re.sub(r'\st="[^"]*"', "", match.group(1))  # číslo nesmí mít typ textu
            xml = xml[: match.start()] + f'<c r="{ref}"{attrs}><v>{value}</v></c>' + xml[match.end() :]
        items[xml_name] = xml.encode("utf-8")

    # Excel má po otevření přepočítat vzorce — jinak by ukazoval staré cache hodnoty.
    wbxml = items["xl/workbook.xml"].decode("utf-8")
    if "<calcPr" in wbxml:
        wbxml = re.sub(r'\sfullCalcOnLoad="[^"]*"', "", wbxml)
        wbxml = re.sub(r"<calcPr([^>]*?)/>", r'<calcPr\1 fullCalcOnLoad="1"/>', wbxml, count=1)
    else:
        wbxml = wbxml.replace("</workbook>", '<calcPr fullCalcOnLoad="1"/></workbook>')
    items["xl/workbook.xml"] = wbxml.encode("utf-8")
    items.pop("xl/calcChain.xml", None)  # neplatný po změně; Excel si ho postaví znovu

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(zipfile.ZipInfo(name, date_time=infos[name].date_time), data)
    return backup


# ---------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="zapsat do sešitu (jinak jen výpis)")
    ap.add_argument("--dry-run", action="store_true", help="jen výpis (výchozí chování)")
    ap.add_argument("--root", type=Path, default=ROOT, help="kořen se složkami vlastníků")
    ap.add_argument("--sporeni", type=Path, default=None, help="cesta k sešitu (výchozí <root>/sporeni.xlsx)")
    ap.add_argument("--no-report", action="store_true", help="neukládat markdown report")
    args = ap.parse_args()

    # Konzole je na Windows cp1250 a české znaky by ji shodily.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    sporeni = args.sporeni or (args.root / "sporeni.xlsx")
    cells, blocks = plan(sporeni, args.root)

    print(console_summary(blocks))

    if args.write:
        backup = write_cells(sporeni, cells)
        print(f"\nZapsáno do {sporeni}")
        print(f"Záloha původního souboru: {backup}")
    else:
        print("\n(jen výpis — do sešitu se nic nezapsalo, zápis provede --write)")

    if not args.no_report:
        suffix = "" if args.write else "_dry-run"
        out = data_dir(PROJECT) / dated(f"xtb_sync{suffix}", ".md")
        out.write_text(markdown_report(blocks, sporeni, args.root, args.write), encoding="utf-8")
        print(f"Report: {out}")


if __name__ == "__main__":
    main()
