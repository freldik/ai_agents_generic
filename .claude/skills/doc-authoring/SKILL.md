---
name: doc-authoring
description: Příprava dokumentů — smlouvy, žádosti, dopisy, reporty, shrnutí — v markdownu, .docx nebo PDF. Použij, když má úloha vytvořit dokument pro člověka, ne data pro stroj.
---

# Příprava dokumentů

## Volba formátu

| Kdy | Formát |
|---|---|
| poznámka, koncept, něco co zůstane v repu | `.md` (Obsidian ho zobrazí) |
| dokument k odeslání nebo tisku, který bude někdo dál upravovat | `.docx` (`python-docx`) |
| finální, needitovatelný | PDF z `.docx` |

Výchozí volba je markdown. Do `.docx` převáděj až když uživatel řekne, že to jde ven.

## Šablony

Opakující se dokumenty ulož jako šablonu do `shared/templates/` s placeholdery
`{{jmeno}}`, `{{datum}}`. Když děláš podobný dokument podruhé, nejdřív se podívej,
jestli tam šablona není.

## Pravidla

1. **Dokumenty česky**, pokud uživatel neřekne jinak. Formální dokumenty vykají.
2. **Nevymýšlej si fakta** — jména, částky, čísla jednacích spisů, datumy.
   Co nevíš, nech jako `[DOPLNIT: …]` a vypiš uživateli seznam těch míst.
3. **Žádné právní ani daňové rady jako fakt.** Můžeš připravit text dokumentu,
   ale u čehokoli se závazky uveď, že to není právní stanovisko.
4. **Datum v dokumentu** = datum vzniku, formát `8. 8. 2026` v textu, `YYYY-MM-DD` v názvu souboru.
5. Hotový dokument ulož do `projects/<name>/` a uživateli napiš cestu — nevypisuj celý obsah do chatu.
