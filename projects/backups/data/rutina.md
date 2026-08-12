# Rutina záloh — co běží samo a co musíš ty

Dohodnuto 2026-08-10. Cíl: ať je ruční jen to, co opravdu nejde jinak.

## 1. Čtvrtletní běh skriptů — `zalohy_ctvrtletni.bat`

**V Plánovači úloh Windows není naplánované nic** (rozhodnuto 2026-08-12). Skripty
pouštíš ručně jedním dávkovým souborem, který je provede po sobě a vypisuje průběh
na obrazovku — kdykoli se dá zastavit Ctrl+C.

```
projects\backups\scripts\zalohy_ctvrtletni.bat
```

| Krok | Co dělá | Jak dlouho |
|---|---|---|
| 1 | `status.py` — co je po termínu ještě před zálohou | vteřiny |
| 2 | `backup_configs.py` — GoodSync, Total Commander, nastavení Thunderbirdu | vteřiny |
| 3 | `backup_data.bat` — Others + Projects do `Data\<Kategorie>\` | **hodiny** |
| 4 | `goodsync_jobs.py` — přepíše dokumentaci jobů z `jobs.tic` | vteřiny |
| 5 | `retention.py --out` — report archivů nad rámec 4+1/rok, **nic nemaže** | vteřiny |
| 6 | `status.py --md` — stav po záloze do `data/status_*.md` | vteřiny |

Pouštěj to **večer** kvůli kroku 3. Průběh se loguje do
`D:\Work\Backup\Data\_log\zalohy_RRRR-MM-DD.log`.

Automatizace přes Plánovač je vědomě zahozená: ruční běh je vidět, dá se zastavit
a nespustí hodinovou archivaci ve chvíli, kdy se to nehodí. Cenou je, že termín si
hlídáš sám — od toho je připomínka v kalendáři.

**Retence nikdy nemaže sama.** Krok 5 jen řekne co a kolik; smazání spouštíš zvlášť
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
22:00 je schválně pozdě večer, ať nekoliduje s ničím, co pouštíš ručně.

**Zálohovací den 1. v měsíci** je tedy: připojit USB (rozjede se samo), v GoodSyncu
ručně spustit skupiny Cloud, Ntb a Monika, nechat doběhnout. Čtyřikrát do roka
k tomu přidáš `zalohy_ctvrtletni.bat` a ruční exporty ze sekce 3.

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
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **Todoist**: ruční export upomínek a úkolů | `D:\Work\Backup\Todoist\` |
| **čtvrtletně** | 1. 1. / 4. / 7. / 10. | **spustit `zalohy_ctvrtletni.bat`** — večer, běží hodiny (viz sekce 1) | — |
| **čtvrtletně** | den poté | **projít `retence_report.md`** z předchozího běhu a případně spustit `retention.py --delete` | — |
| **ročně** | leden | **zkouška obnovy** — viz níže | — |

Nic z toho nejde zautomatizovat: Home Assistant, routery, WD MyCloud i Todoist jsou
za webovým rozhraním a export je klikací. Připojení USB disku je fyzický úkon.
Export pošty z Thunderbirdu klikáš ty; **nastavení** profilu (účty, filtry, adresář)
už zálohuje `backup_configs.py` sám každý měsíc — ruční zůstává jen samotná pošta.

Když na něco zapomeneš, vytkne to `status.py` — buď při dalším čtvrtletním běhu
(kroky 1 a 6), nebo kdykoli si ho pustíš sám. Protože nic neběží na pozadí, je
připomínka v kalendáři jediné, co drží termín.

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
