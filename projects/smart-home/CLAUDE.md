# Projekt: smart-home

## Účel

Obecná dokumentace domácí smart-home instalace — jak se jmenují jednotlivé moduly,
jak je rozvržená síť, jaká je struktura MQTT témat a jak spolu části mluví.
Je to referenční projekt: **primárně dokumentace, ne kód**. Slouží k tomu, aby se
při zásahu do Arduino firmwaru, automatizací nebo sítě dalo dohledat, co kde je.

Zdrojem pravdy je fyzická instalace a repozitáře firmwaru/konfigurací; tenhle projekt
je jejich zapsaný popis.

## Zdrojové adresáře (mimo repo, jen ke čtení)

| Cesta | Co tam je |
|---|---|
| `D:\Electronics\Smart House\Devices` | firmware a konfigurace zařízení, členěno podle lokality |
| `D:\Electronics\Smart House\OpenHab\Last backup` | poslední záloha OpenHABu (2025-04-21) — items, rules, things, sitemap |

Firmware vlastních modulů má navíc git repozitáře na GitLabu
(`home-proj/automation/<nazev>`).

## Data

| Soubor | Co obsahuje | Odkud pochází |
|---|---|---|
| `data/prehled.md` | architektura celku: co jsou vrstvy, kdo s kým mluví — **čti první** | ručně |
| `data/moduly.md` | inventura modulů: název, HW, umístění, firmware, co ovládá | ručně / z Arduino projektů |
| `data/sit.md` | rozvržení sítě: segmenty, rozsahy IP, VLAN, statické adresy, porty | ručně |
| `data/mqtt.md` | soupis MQTT témat, payloady, QoS/retain — **dnešní stav** | ručně / z firmwaru |
| `data/konvence.md` | pravidla pojmenování — **dnešní stav**, dosluhující | ručně |
| `data/konvence_nova.md` | **cílová** konvence po reflashi: témata, zařízení, entity v HA, ESPHome | návrh 2026-08-18 |
| `data/prejmenovani.md` | převod staré téma → nové po zařízeních, se stavem prací | návrh 2026-08-18 |
| `data/kamery.md` | kamery: pojmenování, streamy, Frigate, síťová doporučení | ručně |
| `data/migrace.md` | co z OpenHABu ještě chybí v Home Assistantu a v jakém stavu | ručně / z konfigurace OpenHABu |
| `data/otazky.md` | otevřené otázky na uživatele, seřazené podle důležitosti | ručně; odpovědi se rozvedou do ostatních dokumentů a odsud smažou |

Vstupní data se **nepřepisují**. Výstupy skriptů jdou do `temp/` s datem v názvu
(neverzuje se).

## Skripty

| Skript | Co dělá |
|---|---|
| `scripts/example.py` | kostra z template; zatím se nepoužívá |

**Projekt je čistě dokumentační a takový má zůstat** (rozhodnuto 2026-08-18).
Žádné skripty pro výpis témat z brokeru, kontrolu dostupnosti ani generování
dokumentace z firmwaru — nenavrhuj je.

Spouštění z kořene repa:
`.\.venv\Scripts\python.exe projects/smart-home/scripts/<script>.py`

## Pravidla specifická pro tento projekt

- **Nikdy neměň soubory v dodaném adresáři s Arduino projekty / konfiguracemi.**
  Ten adresář je jen ke čtení; poznatky se přepisují sem do `data/`.
- **Nepublikuj nic do MQTT ani neměň stav zařízení.** Tenhle projekt popisuje,
  neovládá. Jakýkoli zápis do brokeru nebo nahrání firmwaru dělá uživatel.
- **Nehádej.** Když název modulu, IP nebo téma nejde ověřit ve zdroji,
  zapiš ho s `?` a přidej do Otevřených otázek — chybná dokumentace sítě je horší
  než chybějící.
- **Citlivé věci nepatří do gitu.** Wi-Fi hesla, tokeny, API klíče, veřejné IP
  a přesné údaje o zabezpečení → `secrets/` nebo `*_private.md`.
  V dokumentaci na ně jen odkaž („heslo viz secrets“).
- **Probíhá reflash všech zařízení** (přechod OpenHAB → Home Assistant) a s ním
  změna schématu MQTT témat. Platí proto dvě konvence naráz:
  - Nové a přeflashované zařízení → `data/konvence_nova.md`.
  - Nepřeflashované → `data/konvence.md` a `data/mqtt.md`.
  - Který kus je v jakém stavu, říká sloupec „stav“ v `data/prejmenovani.md`.
    **Ten sloupec je jediný zdroj pravdy o postupu migrace** — udržuj ho.
  Až budou všechna zařízení hotová, `konvence.md` a `mqtt.md` se smažou
  a `konvence_nova.md` se přejmenuje na `konvence.md`.
- Když narazíš na výjimku v reálné instalaci, zapiš realitu a označ ji jako výjimku;
  konvenci nepřepisuj zpětně.
- **OpenHAB už neběží** — řídící vrstva je Home Assistant. Konfigurace OpenHABu ale
  pořád existuje a jsou v ní věci, které se do HA teprve přenášejí. Ber ji jako
  **zdroj zadání, ne jako popis provozu**: co je v OpenHABu a ne v HA, patří do
  `data/migrace.md` jako nepřenesené, ne do `data/moduly.md` jako živé.

## Základní fakta (potvrzeno uživatelem 2026-08-18)

- **Home Assistant (HAOS) na Raspberry Pi `192.168.5.22`**, Mosquitto běží jako
  **add-on v HA** — adresa brokeru je vždy adresa HA.
- **Adresy `192.168.0.x` ve firmwaru jsou mrtvé.** Síť byla přečíslována; žádné
  staré zařízení se dnes k brokeru nepřipojí. Nikdy je nepoužívej jako platné.
- Chystá se **VLAN pro smart home a kamery** → nové SSID → **SSID musí být
  známé před flashováním**, je ve firmwaru natvrdo.
- **TLS na brokeru se zapíná při reflashi.**
- Co půjde, přepíše se do **ESPHome**; smart hodiny zůstanou s vlastním kódem.

## Otevřené otázky

- **Nic z dokumentace není ověřené proti dnešnímu Home Assistantu** — všechno
  pochází z firmwaru zařízení a ze zálohy OpenHABu. Až bude po ruce konfigurace HA,
  projít a označit, co platí.
- Zbytek otevřených otázek je v `data/otazky.md` a u jednotlivých dokumentů.
