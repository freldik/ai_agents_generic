# ai_agents_generic

Osobní pracovní repozitář pro agentní úlohy — práce s Excelem (nákupy, sledování akcií),
příprava dokumentů a další domácí agenda. Zároveň je to Obsidian vault, takže poznámky
jsou markdown a mají být čitelné i bez agenta.

## Struktura

| Cesta | Účel |
|---|---|
| `projects/<name>/` | samostatný projekt, nezávislý na ostatních |
| `projects/_template/` | kostra pro nový projekt — zkopíruj ji |
| `shared/lib/` | sdílené python utility |
| `shared/templates/` | sdílené šablony dokumentů (.xlsx, .docx, .md) |
| `.claude/skills/` | dovednosti sdílené napříč projekty (jak něco dělat) |

## Pravidla závislostí

- **Projekt nikdy neimportuje jiný projekt.** Sdílet lze jen přes `shared/` a skills.
- **Skills = jak, projects = co.** Postup („jak zapsat xlsx bez rozbití formátování")
  patří do skillu. Data a konkrétní zadání („které tickery sleduju") do projektu.
- Nový projekt = kopie `projects/_template/`. Nesmí být potřeba měnit nic jinde.

## Prostředí

Jedno sdílené venv v kořeni: `.venv/`. Závislosti v `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Skripty spouštěj přes `.\.venv\Scripts\python.exe projects/<name>/scripts/<script>.py`.

Aby šlo importovat `shared/`, skripty na začátku přidají kořen repa do `sys.path`:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from shared.lib import excel_io
```

## Konvence

- **Jazyk:** poznámky a dokumenty česky, kód a commit messages anglicky.
- **Datumy:** vždy `YYYY-MM-DD`, nikdy relativně („minulý týden") v uložených souborech.
- **Data se verzují.** Historie portfolia i nákupů je hodnotná.
  Citlivé soubory pojmenuj `*_private.*` nebo ulož do `secrets/` — to je gitignorováno.
- **Nikdy nepřepisuj vstupní data.** Výstupy piš vedle nich s datem v názvu.
- Před přepsáním existujícího `.xlsx` se zeptej — často obsahuje ruční úpravy.
