# Otázky k zodpovězení

> Původně sepsáno 2026-08-13, **první kolo odpovědí zpracováno 2026-08-18** —
> zodpovězené otázky jsou rozvedené v příslušných dokumentech a odsud smazané.
> Zbývá to, co uživatel odložil na později, plus otázky, které z odpovědí nově
> vyplynuly.
>
> Odpovědi piš rovnou pod otázku. Pořadí je podle toho, jak moc odpověď
> odblokuje zbytek práce.

---

## A. Blokuje reflash

Tohle jde do firmwaru natvrdo. Rozhodnout **před** flashnutím prvního kusu,
jinak se flashuje dvakrát. Viz [prejmenovani](prejmenovani.md).

### A1. Jaké SSID a heslo bude mít smart-home Wi-Fi?
Rozhodnuto, že vznikne samostatná VLAN se svým routerem a Wi-Fi
([sit](sit.md)). Dokud není jméno a heslo, nemá smysl flashovat — SSID
je v `.ino` i v ESPHome YAML natvrdo.

> odpověď:

### A2. Bude smart home a kamery jedna VLAN, nebo dvě?
Šest Wi-Fi kamer na stejné rádiové síti jako ESP moduly znamená video stream
vedle krátkých MQTT paketů. Doporučuju dvě.

> odpověď:

### A3. TLS na brokeru — vlastní CA, nebo Let's Encrypt?
Rozhodnuto TLS zapnout. Pro domácí síť stačí vlastní CA, ale certifikát musí mít
v SAN **IP `192.168.5.22`** (ESP se připojuje na IP, ne na jméno). Certifikát
musí existovat dřív než první flash.

> odpověď:

### A4. Terasová světla — které je `wall_light_l` a které `_r`?
Při pohledu odkud? Zatím odhad. Prohozené strany se v HA opravují hůř než
v konfiguraci, takže tahle dvě zařízení flashuj až po odpovědi. (dřív G3)

> odpověď:

---

## B. Ověření dnešního stavu

### B1. Které moduly jsou živé?
Projít seznam v [moduly](moduly.md) a označit: běží / neběží / vyhozené.
Zvlášť ty bez složky v `Devices`: teplota+vlhkost pracovna, čidlo světla
pracovna, hodiny pracovna, čidlo teploty zahrada.

Pozn.: zařízení mají v konfiguraci neplatnou adresu brokeru (`192.168.0.x`),
takže „běží“ dnes znamená „je napájené a připojené k Wi-Fi“, ne „posílá data“.

> odpověď: (uživatel dodá později)

### B2. Konfigurace Home Assistanta
Cesta k `configuration.yaml` / `.storage`, nebo záloha. Bez toho nejde ověřit
**nic** z toho, co je dnes reálně živé — a je to jediné místo, kde jsou vidět
ručně definované `mqtt:` entity. (dřív A2)

> odpověď: (uživatel dodá později)

### B3. Které automatizace už jsou v Home Assistantu hotové?
Seznam funkcí je v [migrace](migrace.md), vše je zatím `nepřeneseno`.
Stačí říct, které řádky jsou hotové — přepíšu stavy.

> odpověď: (uživatel dodá později)

---

## C. Hardware

### C1. Doplnit typ HW u 4 Sonoffů
V `my_user_config.h` chybí `MODULE` u: světlo pracovna, světlo zahradní domek,
terasa switch 1, terasa switch 2.

> odpověď: (uživatel dodá později)

### C2. Kde která ze tří AP fyzicky je?
`freldik_ntw`, `freldik_ntw_liv`, `freldik_ntw_garden`. Rozhoduje o pokrytí
zahradních modulů a kamer — a o tom, kam umístit AP nové smart-home VLAN.
(dřív D1)

> odpověď: (uživatel dodá později)

### C3. Které kamery jsou Reolink a které Tapo?
Modely a rozlišení. RTSP cesta se u obou značek liší, bez modelu ji nedohledám.
(dřív G1)

> odpověď:

### C4. Co znamenají adresy v `ip.txt` (`192.168.0.105/109/113/120`)?
Beru je jako „adresa v době konfigurace“, ne jako rezervaci — po přečíslování
sítě jsou tak jako tak mrtvé. A co znamenají čísla typu `Number: 1674`
a `light_switch-1459` v týchž souborech? (dřív D3)

> odpověď:

---

## D. Až přijde na řadu

### D1. Jaký konkrétní Mikrotik a jaké má rozsahy?
Model, IP brány, DHCP pool, jestli dělá i DNS. Potřeba k naplánování rezervací
a VLAN.

> odpověď:

### D2. Spí bazénové čidlo v deep sleep?
Z kódu to potvrzené není. Rozhoduje o tom, jestli u něj má LWT vůbec smysl
a jestli mu zapínat TLS.

> odpověď:

### D3. Kolik historie ze kamer držet, až bude NAS?
Určuje kapacitu disku. Dnes jen SD karty v kamerách.

> odpověď:

---

## Zpracované odpovědi (2026-08-18)

Kam se rozvedly, kdyby bylo potřeba dohledat:

| Téma | Kam to šlo |
|---|---|
| HA na HAOS, `192.168.5.22`; Mosquitto jako add-on; jeden broker | [sit](sit.md), [mqtt](mqtt.md), [prehled](prehled.md) |
| Staré adresy `192.168.0.52/.106` jsou neplatné | [sit](sit.md), [mqtt](mqtt.md), [moduly](moduly.md) |
| 3D tiskárna zrušena, Bambulab P2S | [moduly](moduly.md), [mqtt](mqtt.md), [prejmenovani](prejmenovani.md), [migrace](migrace.md) |
| Entity v HA definované ručně (cíl: discovery) | [mqtt](mqtt.md), [konvence_nova](konvence_nova.md) |
| Broker přeinstalován, žádná retained „duchy“ | [mqtt](mqtt.md), [prejmenovani](prejmenovani.md) |
| Desky: ESP-07, hodiny ESP32-WROOM | [moduly](moduly.md) |
| Tasmota: nedávno aktualizováno, při reflashi nejnovější | [moduly](moduly.md) |
| Firmware zčásti jen lokálně, zčásti v gitu | [moduly](moduly.md), [prehled](prehled.md) |
| Flashuje se kabelem, cíl OTA všude | [moduly](moduly.md), [konvence_nova](konvence_nova.md) |
| VLAN pro smart home i kamery (mění dřívější doporučení) | [sit](sit.md), [konvence_nova](konvence_nova.md) |
| DHCP: Mikrotik; zařízení dynamicky, kamery staticky | [sit](sit.md) |
| Ven nic vystaveno, HA Cloud placený, openHAB Cloud zrušen | [sit](sit.md), [migrace](migrace.md) |
| Kamery Reolink + Tapo, Wi-Fi, SD karta, Frigate až s NAS | [kamery](kamery.md), [sit](sit.md) |
| Schéma témat i přesun terasy do `around` potvrzeny | [konvence_nova](konvence_nova.md), [prejmenovani](prejmenovani.md) |
| ESPHome kde to jde, hodiny vlastní kód | [konvence_nova](konvence_nova.md) |
| TLS na brokeru se zapne | [konvence_nova](konvence_nova.md), [prejmenovani](prejmenovani.md) |
| 433 MHz zůstává, Zigbee možná později | [migrace](migrace.md), [prejmenovani](prejmenovani.md) |
| LWT doplnit všude | [konvence_nova](konvence_nova.md) |
| Notifikace do HA app | [migrace](migrace.md) |
| Siréna a uzávěr vody nebyly nikdy implementované | [migrace](migrace.md) |
| Projekt zůstává dokumentační, bez skriptů | `CLAUDE.md` |
| Alexa se používá (obývák, ložnice) | [moduly](moduly.md), [migrace](migrace.md) |
| Bazénové čidlo zůstává na baterii | [prejmenovani](prejmenovani.md), [migrace](migrace.md) |
| Zálohy HA v cloudu + měsíční ruční stažení | [migrace](migrace.md) |
