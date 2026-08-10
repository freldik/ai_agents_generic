# Rutina záloh — co běží samo a co musíš ty

Dohodnuto 2026-08-10. Cíl: ať je ruční jen to, co opravdu nejde jinak.

## 1. Naplánované úlohy Windows

Vytvoří je `scripts/install_tasks.ps1 -Install`, zruší `-Uninstall`.
Všechny běží pod tvým účtem (potřebují `M:`, `%APPDATA%`) a mají zapnuté
„spustit při nejbližší příležitosti", takže vypnutý počítač je jen odklad.

| Kdy | Úloha | Co dělá | Jak dlouho |
|---|---|---|---|
| 1. každý měsíc ve 20:30 | Zálohy - konfigurace | GoodSync, Total Commander, nastavení Thunderbirdu | vteřiny |
| 1. každý měsíc ve 20:35 | Zálohy - seznam GoodSync jobů | přepíše dokumentaci z `jobs.tic` | vteřiny |
| 2. 1. / 4. / 7. / 10. ve 20:00 | Zálohy - RAR archivy | `backup_data.bat` — Others + Projects do `Data\<Kategorie>\` | hodiny |
| 3. každý měsíc ve 20:00 | Zálohy - retence (jen report) | vypíše archivy nad rámec 4+1/rok do `D:\Work\Backup\Data\_log\retence_report.md` | vteřiny |
| každé pondělí v 18:00 | Zálohy - kontrola stavu | `status.py --md` — co je po termínu | vteřiny |

Dny jdou schválně po sobě. **1.** je tvůj ruční večer (USB, GoodSync, čtvrtletní
exporty) a drobné úlohy k němu; **2.** běží RAR archivace, která trvá hodiny a
nemá ti do toho večera lézt; **3.** vznikne report retence, který tak už vidí
i čerstvý archiv z předchozího dne.

**Retence nikdy nemaže sama.** Report jen řekne co a kolik; smazání spouštíš ty
(`retention.py --delete`, ptá se na potvrzení). Tak to má zůstat.

Čtvrtletní RAR je záměr, ne kompromis: archiv má ~20 GB a kompletní data jsou i tak
každý den v GoodSyncu. RAR je pojistka proti „smazal jsem to před půl rokem a nevšiml
si toho", ne denní záloha.

## 2. GoodSync — periodicita

Automaticky jede jen to, co neruší práci. Synchronizace na `M:` trvá u některých
projektů dlouho a zatěžuje síť, takže zůstává ruční — ale s pevným termínem,
ne „až si vzpomenu". Proto **1. v měsíci je zálohovací den**.

| Skupina | Jobů | Periodicita | Nastavení v GoodSync |
|---|---|---|---|
| **OneDrive** (`D:\OneDrive`) | 8 | **automaticky denně ve 22:00** | Job → Options → Auto → *Auto Sync: On Schedule*, denně 22:00 |
| **Cloud** (`M:` WD MyCloud) | 7 | **ručně 1. v měsíci** | nechat *Auto Sync* vypnutý, spouštět z GUI |
| **Ntb** (`N:` pracovní notebook) | 5 | **ručně 1. v měsíci** | dtto |
| `Monika - Ntb` (`L:`) | 1 | **ručně 1. v měsíci**, když je notebook zapnutý | dtto; naposled 2025-07-27 |
| **Disk WD** (USB My Passport) | 8 | **při připojení disku** — USB připojuješ 1. v měsíci | Auto → *On Device Connect* |

Jen OneDrive je bezpečné pouštět denně: je to lokální disk `D:`, žádná síť.
22:00 je schválně po naplánovaných úlohách ve 20:00–20:35.

**Zálohovací den 1. v měsíci** je tedy: připojit USB (rozjede se samo), v GoodSyncu
ručně spustit skupiny Cloud, Ntb a Monika, nechat doběhnout. Naplánované úlohy
(konfigurace, seznam jobů) běží tentýž večer samy.

GoodSync startuje s Windows, takže se nic neplánuje ve Správci úloh — periodicita
se nastavuje v jobech samotných.

Až bude NAS s RAIDem, tohle se překreslí — RAID nahradí USB disk jako druhou kopii
a `On Device Connect` přestane být potřeba.

## 3. Co zůstane ručně — připomínky do kalendáře

Tohle je ta část, kterou si dej do telefonu jako opakovanou událost. Všechno ostatní
běží samo.

Čtvrtletní věci jsou schválně nasypané na **1. leden / duben / červenec / říjen** —
je to tentýž den jako měsíční synchronizační kolo, takže čtyřikrát do roka si sedneš
na hodinu ke všemu najednou a zbylých osm měsíců je jen připojení USB a kliknutí
v GoodSyncu.

| Perioda | Kdy | Co udělat | Kam to uložit |
|---|---|---|---|
| **měsíčně** | 1. v měsíci | **připojit USB disk My Passport** — joby se rozjedou samy | — |
| **měsíčně** | 1. v měsíci | **v GoodSyncu ručně spustit** skupiny Cloud (`M:`), Ntb (`N:`) a Monika (`L:`) | — |
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **Home Assistant**: stáhnout zálohu z Nabu Casa | `D:\Work\Backup\HomeAssistant\` |
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **routery a AP**: export konfigurace (Mikrotik Attic, TP-Link Archer AX10 Obývák a Hůra, opakovače) | `D:\Work\Backup\Router\<zařízení>\` |
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **WD MyCloud**: export nastavení `.conf` | `D:\Work\Backup\WD MyCloud\` |
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **Thunderbird**: export pošty obou účtů | `D:\Work\Backup\Thunderbird\<účet>\RRRR_MM\` |
| **čtvrtletně** | 4. 1. / 4. / 7. / 10. | **projít `retence_report.md`** (vznikl předchozí večer) a spustit `retention.py --delete` | — |
| **ročně** | leden | **zkouška obnovy** — viz níže | — |

Nic z toho nejde zautomatizovat: Home Assistant, routery i WD MyCloud jsou za
webovým rozhraním a export je klikací. Připojení USB disku je fyzický úkon.
Export pošty z Thunderbirdu klikáš ty; **nastavení** profilu (účty, filtry, adresář)
už zálohuje `backup_configs.py` sám každý měsíc — ruční zůstává jen samotná pošta.

Když na něco zapomeneš, `status.py` to v pondělní kontrole vytkne. To je ta pojistka —
připomínka v kalendáři se dá odklepnout, report po termínu se hromadí.

## 4. Zkouška obnovy (jednou ročně)

Nikdy neproběhla. Nemusí být velká, stačí půl hodiny:

1. Rozbalit **náhodných pár složek** z posledního `Projects_*.rar` do dočasné složky
   a porovnat s originálem.
2. Vzít **jeden soubor z `M:\Backup\Desktop\...`** a ověřit, že je čitelný a aktuální.
3. Otevřít poslední **Home Assistant `.tar`** a zkontrolovat, že v něm je
   `homeassistant.tar.gz`, ne prázdný obal.
4. Zapsat datum a výsledek do `data/inventory.md`.

Bod 3 je důležitý — HA zálohy se stahují ručně a nikdo se do nich nikdy nepodíval.

## 5. Co vědomě nezálohujeme

Rozhodnuto 2026-08-10, ať se to znovu neotevírá:

- **`D:\School` a `D:\Led neons`** — historické věci, stačí jedna kopie v OneDrive.
  Nerozšiřovat na MyCloud ani USB.
- **Obsah WD MyCloud** — druhá kopie je v OneDrive, samotný disk se nezálohuje.
  Přehodnotit až s NAS.
- **OpenHAB** — přešlo se na Home Assistant, položka je uzavřená.
