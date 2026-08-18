# Smart home — přehled

> Zapsáno 2026-08-13 z `D:\Electronics\Smart House\Devices` a z poslední zálohy
> OpenHABu (2025-04-21), doplněno odpověďmi uživatele 2026-08-18. Popisuje
> **stav, jak ho zachytil OpenHAB** — co z toho dnes běží pod Home Assistantem,
> ověřeno není, viz [migrace](migrace.md).

## Vrstvy

| Vrstva | Co to je | Konkrétně |
|---|---|---|
| Zařízení | 14 Tasmota Sonoffů + 6 vlastních ESP modulů + ~15 čidel na 433 MHz | [moduly](moduly.md) |
| Kamery | 6 IP kamer Reolink + TP-Link Tapo, Wi-Fi, záznam na SD — mimo MQTT | [kamery](kamery.md) |
| Přenos | Wi-Fi (3 SSID) → MQTT | [sit](sit.md) |
| Broker | Mosquitto jako **add-on v HA**, `192.168.5.22:1883`, s heslem, bez TLS | [mqtt](mqtt.md) |
| Řízení | **Home Assistant (HAOS)** na Raspberry Pi `192.168.5.22`, dřív OpenHAB | [migrace](migrace.md) |

Řízení i broker běží na jednom Raspberry Pi. Je to jediný bod selhání pro celý
dům — restart HA je zároveň restart brokeru.

## Probíhá přestavba

Přechod z OpenHABu na Home Assistant znamená **přeflashovat všechna zařízení**.
Toho se využívá k narovnání schématu MQTT témat, které mělo prefix uprostřed
cesty a lokalitu proměnné hloubky — obojí znemožňovalo wildcard odběry.

| Dokument | Co v něm je |
|---|---|
| [konvence_nova](konvence_nova.md) | **cílová** konvence: témata, zařízení, entity v HA, ESPHome |
| [prejmenovani](prejmenovani.md) | převod staré téma → nové, po zařízeních, se stavem prací |
| [konvence](konvence.md), [mqtt](mqtt.md) | **dosluhující** stav — platí pro nepřeflashovaná zařízení |

Dokud běží obojí, je nutné u každého zařízení vědět, kterým schématem mluví.
Stav je ve sloupci „stav“ v [prejmenovani](prejmenovani.md).

## Tok dat

```
                        Raspberry Pi 192.168.5.22 (HAOS)
                        ┌──────────────────────────────┐
[Tasmota Sonoff] --+    │                              │
[vlastní ESP]    --+--> │ Mosquitto :1883 --> Home Assistant │ --> UI / automatizace
                   |    │        ^                     │           notifikace do HA app
[433 MHz čidlo] -> [RF bridge] --tele/rfbridge/RESULT   │
                        │        |                     │
                        │  <lokalita>/cmnd/<zařízení>/… │
                        └──────────────────────────────┘
[IP kamera] --RTSP--> (dnes nikam, jen SD karta v kameře)
[Alexa] --cloud--> Home Assistant
```

Kamery do MQTT nevstupují a dnes se nikam centrálně nenahrávají. Hlasové
ovládání jde přes Amazon Echo (obývák, ložnice).

433 MHz čidla (voda, pohyb, dveře, ovladače alarmu) nemluví MQTT sama — jde to
přes RF bridge v pracovně, který jejich kód publikuje jako jedno téma. **Bridge je
jediný bod selhání pro alarm i hlídání úniku vody.**

## Rozdělení podle lokality

- `house/` — pracovna, obývák, kuchyň, ložnice, půda, chodba
- `around/` — garáž, balkon
- `garden/` — zahrada, zahradní domek, bazén, terasa (terasa je historicky u zahrady)

## Co kde hledat

- Jak pojmenovat nové zařízení / entitu v HA → [konvence_nova](konvence_nova.md)
- Jak přeflashovat konkrétní modul → [prejmenovani](prejmenovani.md)
- Kamery → [kamery](kamery.md)
- Pravidla pojmenování a výjimky ve starém schématu → [konvence](konvence.md)
- Konkrétní modul (kde je, jaká deska, jaké téma) → [moduly](moduly.md)
- Téma, payload, retain → [mqtt](mqtt.md)
- IP adresa, SSID, broker → [sit](sit.md)
- Co z OpenHABu ještě chybí v HA → [migrace](migrace.md)
- Hesla, RF kódy alarmu → `secrets/` (mimo git)

## Známá slabá místa

- **Adresa brokeru se změnila na `192.168.5.22`**, ale firmware všech zařízení
  má pořád `192.168.0.52` / `.106`. Bez reflashe se nepřipojí nic.
- **Vlastní moduly nemají LWT** — výpadek modulu není přímo poznat. Doplní se
  při reflashi (rozhodnuto).
- **SSID je ve firmwaru natvrdo** — změna Wi-Fi = reflash všech vlastních modulů.
  Chystaná smart-home VLAN tím pádem musí mít SSID určené **před** flashováním.
- **Alarm a únik vody visí na jednom RF bridge** bez zálohy. Zůstává na 433 MHz,
  Zigbee je až budoucí úvaha.
- **HA i broker běží na jednom Raspberry Pi** — jeden bod selhání pro celý dům.
- **Kamery nahrávají jen na SD karty v sobě.** Kdo kameru ukradne, ukradne
  i záznam. Centrální úložiště (NAS + Frigate) je plán, ne stav.
- Firmware vlastních modulů žije v samostatných git repozitářích na GitLabu,
  ale zdrojáky jsou i lokálně v `Devices` — **část je jen lokálně** a rozešlo
  se to. Uživatel plánuje srovnat.

## Otevřené otázky

- Co z automatizací už je reálně v HA? Neověřeno, viz [migrace](migrace.md).
- Konfigurace HA (`configuration.yaml`, `.storage`) zatím není k dispozici —
  dokud nebude, je popis živého stavu odhad z firmwaru a ze zálohy OpenHABu.
