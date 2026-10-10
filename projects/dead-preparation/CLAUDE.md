# Projekt: dead-preparation

## Účel

Připravit pro rodinu všechno, co by potřebovala, kdyby se uživateli něco stalo —
finance, přístupy a hesla, dům, auta a další agendu — tak, aby se v tom zorientovala
bez něj a bez agenta.

## Kde jsou data — POZOR, repo je veřejné

Repozitář je **veřejný na GitHubu**. Tady v repu je proto jen **obecná kostra**:
tenhle soubor a osnova v `data/osnova.md`. Žádná jména, instituce, čísla účtů,
adresy, umístění hesel ani nic jiného osobního.

**Skutečný obsah je mimo repo, v `D:\Others\Pozustalost\`** (rozhodnuto 2026-10-01):

- neverzuje se v gitu,
- zálohuje se jako celé `D:\Others` (GoodSync na WD MyCloud a USB disk, čtvrtletní RAR
  — viz projekt `backups`), do cloudu nejde,
- je to obyčejný markdown, čitelný v Obsidianu i v Poznámkovém bloku, bez agenta.

| Soubor v `D:\Others\Pozustalost\` | Obsah |
|---|---|
| `00_ZACNI_TADY.md` | rozcestník pro rodinu: co dělat první dny a týdny, kde co je |
| `01_kontakty.md` | lidé a instituce, kterým zavolat |
| `02_finance.md` | účty, investice, penze, pojistky, úvěry, platby, OSVČ, finanční plán |
| `03_hesla_a_pristupy.md` | správce hesel, nouzový přístup, 2FA, e-mail, iPhone, trezor |
| `04_dum.md` | údržba v kalendáři, chytrá domácnost, síť, energie, dokumenty k domu |
| `05_auta.md` | auta a motorky: pojistky, STK, servis, doklady |
| `06_ostatni.md` | digitální účty, předplatné, fotky a zálohy, doklady, poslední přání |

Odkazy na dokumenty vedou do sousedních složek `D:\Others\…` (Banky, Dum, Auta, Doklady…),
kde už originály leží — nic se nekopíruje.

## Pravidla

- **Do repa nikdy nic osobního.** Při práci na projektu piš obsah jen do
  `D:\Others\Pozustalost\`. Když si nejsi jistý, jestli údaj je osobní, je.
- **Hesla se nezapisují nikam** — ani do `D:\Others\Pozustalost\`. Dokumenty říkají
  *kde* heslo je a *jak* se k němu rodina dostane (správce hesel, nouzový přístup,
  obálka v trezoru), nikdy heslo samotné. Totéž PIN, kód trezoru, záchranné kódy.
- Psáno pro člověka, který se v tom nevyzná: krátké věty, konkrétní kroky, žádný žargon.
  Žádné „viz repo“ — rodina repo otevírat nebude.
- Každý soubor má nahoře datum poslední kontroly (`YYYY-MM-DD`).
- Nevyplněné údaje jsou označené `TODO:` — díky tomu jdou dohledat (`grep TODO`).

## Údržba

- **Kontrola jednou ročně** (a po každé velké změně — nový účet, auto, pojistka, banka).
  Projít `TODO:`, aktualizovat data kontroly.
- Vytištěná verze `00_ZACNI_TADY.md` patří k fyzickým dokumentům — po změně vytisknout znovu.

## Otevřené otázky

- Jak se rodina dostane k samotnému počítači a k `D:\Others\Pozustalost\`
  (heslo do Windows, kopie na disku, tištěná verze)?
- Nastavit nouzový přístup ve správci hesel a Apple Digital Legacy — zatím nevyřešeno.
- Je potřeba závěť / plná moc / dispoziční právo k účtům? (řeší notář, ne tento projekt)
