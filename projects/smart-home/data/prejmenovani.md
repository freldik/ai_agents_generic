# Převod témat: staré → nové

> Sepsáno 2026-08-18. Pracovní seznam pro reflash při přechodu na Home Assistant.
> Cílová pravidla jsou v [konvence_nova](konvence_nova.md), dnešní stav
> v [mqtt](mqtt.md).

## Jak to používat

Sloupec **stav** je jediné místo, kde je vidět, co je hotové:

- `todo` — zařízení mluví starým schématem
- `flashed (YYYY-MM-DD)` — přeflashované, mluví novým schématem
- `v HA (YYYY-MM-DD)` — navíc ověřeno, že entity v HA sedí a chodí data
- `zrušeno` — zařízení se nevrací, důvod do poznámky

**Zapisuj stav hned při flashi, ne dodatečně.** Rozpracovaná migrace, kde není
vidět, kdo mluví kterým schématem, je horší než obě schémata zvlášť.

## Co musí být hotové, než se flashne první kus

Tyhle tři věci jdou do firmwaru natvrdo. Když se rozhodnou až v půlce, flashuje
se dvakrát.

| Věc | Stav | Hodnota |
|---|---|---|
| **Adresa brokeru** | ✅ vyřešeno | `192.168.5.22` (Mosquitto add-on v HA) |
| **SSID a heslo smart-home VLAN** | ❌ **blokuje** | VLAN se teprve staví, viz [sit](sit.md) |
| **TLS certifikát brokeru** | ❌ **blokuje** | rozhodnuto zapnout, CA zatím není |

## Pořadí prací

1. **Postavit smart-home VLAN a určit SSID + heslo.** Bez toho nemá smysl
   začínat — SSID je ve firmwaru natvrdo.
2. **Zapnout TLS na Mosquittu** a mít certifikát (SAN musí obsahovat
   `192.168.5.22`). Port `8883` vedle `1883`, dokud neběží všechno.
3. **Jedno zařízení celé** (firmware → discovery → entity v HA → ověřit data),
   teprve pak další. Ne „všechno přeflashovat a pak řešit HA“.
4. **Začít nekritickými** — vánoční světla, zásuvky. Alarm, únik vody a detektor
   kouře až na konec, s ověřením, že poplach reálně dorazí.
5. **Hodiny až úplně nakonec** — berou si data přímo z brokeru, takže jejich
   zdroje musí být přeflashované dřív.

**Čištění retained témat odpadá.** Broker byl s HAOS nainstalovaný znovu, staré
retained zprávy po OpenHABu v něm nejsou. Pokud přesto něco uvidíš v
`mosquitto_sub -t '#' -v`, publikoval to živý modul — ne duch.

**Zařízení nekomunikují už teď.** Mají v konfiguraci `192.168.0.52`/`.106`,
což je adresa, která neexistuje. Reflash tedy nic nerozbije — rozbité to je.

## Tasmota zařízení

`FullTopic` nově `%prefix%/<lokalita>/<zona>/%topic%/` — prefix vepředu je
u Tasmoty nativní, jde tedy jen o změnu jednoho řetězce v konfiguraci.

| Zařízení | Staré téma | Nové téma | Stav |
|---|---|---|---|
| Světlo pracovna | `house/workroom/{stat,cmnd}/switch/POWER` | `{stat,cmnd}/house/workroom/ceiling_light/POWER` | todo |
| Zásuvka pracovna | `house/workroom/{stat,cmnd}/socket/POWER` | `{stat,cmnd}/house/workroom/socket/POWER` | todo |
| RF bridge | `house/workroom/tele/rfbridge/RESULT` | `tele/house/workroom/rf_bridge/RESULT` | todo |
| Zásuvka obývák | `house/livroom/{stat,cmnd}/socket/POWER` | `{stat,cmnd}/house/livroom/socket/POWER` | todo |
| Vánoční komín | `house/livroom/{stat,cmnd}/socket2/POWER` | `{stat,cmnd}/house/livroom/xmas_chimney/POWER` | todo |
| Dotyk obývák | `house/livroom/{stat,cmnd}/wall_touch/POWER1,2` | `{stat,cmnd}/house/livroom/switch_panel/POWER1,2` | todo |
| Zásuvka kuchyň | `house/kitchen/{stat,cmnd}/socket/POWER` | `{stat,cmnd}/house/kitchen/socket/POWER` | todo |
| Zásuvka ložnice | `house/bedroom/{stat,cmnd}/socket/POWER` | `{stat,cmnd}/house/bedroom/socket/POWER` | todo |
| Dotyk garáž | `around/garage/{stat,cmnd}/wall_touch/POWER1,2` | `{stat,cmnd}/around/garage/switch_panel/POWER1,2` | todo |
| Vánoční balkon | `around/balcony/{stat,cmnd}/light_switch/POWER` | `{stat,cmnd}/around/balcony/xmas_balcony/POWER` | todo |
| Světlo terasa zeď 1 | `garden/{stat,cmnd}/light_switch1/POWER` | `{stat,cmnd}/around/terrace/wall_light_l/POWER` | todo |
| Světlo terasa zeď 2 | `garden/{stat,cmnd}/light_switch2/POWER` | `{stat,cmnd}/around/terrace/wall_light_r/POWER` | todo |
| Světlo zahradní domek | `garden/house/{stat,cmnd}/light_out/POWER` | `{stat,cmnd}/garden/house/outdoor_light/POWER` | todo |
| Vánoční zahradní domek | `garden/house/{stat,cmnd}/light_switch/POWER` | `{stat,cmnd}/garden/house/xmas_garden_house/POWER` | todo |

**Terasa se stěhuje z `garden` do `around/terrace`** (potvrzeno uživatelem
2026-08-18). Je to největší přesun v seznamu — zkontroluj, že na `garden/…`
nezůstane nic z terasy.

**`wall_light_l` / `wall_light_r`** — potřebuju vědět, které fyzicky je které
(při pohledu odkud?), abych to zapsal správně. Zatím jen odhad; uživatel doplní,
až se to začne rozchazet (otázka A4). Do té doby **neflashuj terasová světla** —
prohozené `l`/`r` se v HA opravuje hůř než v konfiguraci.

Telemetrie se přesouvá s nimi: `tele/<lokalita>/<zona>/<topic>/{LWT,STATE,INFO1..3}`.

## Vlastní ESP moduly

Tady je změna větší — kromě tématu přibývá **LWT** a **discovery**, a mění se
client id. Doporučení: nepřepisovat `.ino`, ale přepsat modul do ESPHome
(viz [konvence_nova](konvence_nova.md)). U hodin to nejspíš nepůjde — mají
vlastní logiku displeje.

### Topení skříň garáž

Repo `wardrobe_heater` → `garage_wardrobe_heater`, client id
`ESP8266ClientWardrobeHeater` → `garage-wardrobe-heater`.

| Staré | Nové |
|---|---|
| `around/garage/stat/wardrobe/temp` | `stat/around/garage/wardrobe_heater/temp` |
| `around/garage/stat/air/temp` | `stat/around/garage/wardrobe_heater/air_temp` |
| `around/garage/stat/wardrobe/tempset` | `stat/around/garage/wardrobe_heater/tempset` |
| `around/garage/cmnd/wardrobe/tempset` | `cmnd/around/garage/wardrobe_heater/tempset` (retained) |
| `around/garage/{stat,cmnd}/heat_switch/heat` | `{stat,cmnd}/around/garage/wardrobe_heater/heat` |
| — | `tele/around/garage/wardrobe_heater/LWT` (nové) |

Stav: todo

V HA to má být **`climate`** entita, ne tři samostatné senzory a spínač — má
teplotu, žádanou teplotu i výstup. Discovery komponenta `climate`.

### Teplota + světlo zahradní domek

Repo `temp_light_module` → `garden_house_temp_light`, client id
`garden-house-temp-light`.

| Staré | Nové |
|---|---|
| `garden/house/stat/temp` | `stat/garden/house/temp_light/temp` |
| `garden/stat/temp` | `stat/garden/main/temp_light/outdoor_temp` |
| `garden/stat/light` | `stat/garden/main/temp_light/light` |
| — | `tele/garden/house/temp_light/LWT` (nové) |

Stav: todo

Modul má dvě čidla ve dvou zónách. Nově je obě publikuje **pod svojí zónou**
(`garden/house`) s rozlišením ve `<vec>` — `outdoor_temp` vedle `temp`. Dřív
bylo venkovní čidlo pod `garden/`, což vypadalo jako samostatné zařízení.
Zařazení do zóny `Zahrada` se udělá v HA nastavením oblasti u entity.

### Smart hodiny zahradní domek

Repo `smart_clock` → `garden_house_clock`, client id `garden-house-clock`.

| Staré (odebírá) | Nové |
|---|---|
| `garden/stat/temp` | `stat/garden/house/temp_light/outdoor_temp` |
| `garden/pool/stat/temp` | `stat/garden/pool/pool_sensor/temp` |
| `garden/stat/light` | `stat/garden/house/temp_light/light` |
| `garden/house/cmnd/clock/value` | `cmnd/garden/house/clock/value` |
| `garden/house/cmnd/clock/POWER` | `cmnd/garden/house/clock/POWER` (retained) |
| `house/workroom/stat/light` | `stat/house/workroom/light_sensor/light` |
| `house/workroom/cmnd/clock/POWER` | `cmnd/house/workroom/clock/POWER` (retained) |
| — | `tele/garden/house/clock/LWT` (nové) |

Stav: todo

**Pozor:** hodiny mají dvě varianty buildu (zahradní domek a pracovna) a každá
odebírá jiná témata. Přeflashovat obě a nezapomenout, že varianta pro pracovnu
používá `freldik_ntw`. Client id druhé varianty `workroom-clock`.

Tenhle modul je jediný, u kterého se **nedá vynechat MQTT** ve prospěch nativního
API — bere si data přímo z brokeru. Ostatní zdroje musí být přeflashované dřív
než hodiny, jinak přestanou zobrazovat.

### Teplota půda

Repo `temperature_esp32` → `attic_temp`, client id `attic-temp`.

| Staré | Nové |
|---|---|
| `house/attic/stat/temp` | `stat/house/attic/attic_temp/temp` |
| — | `tele/house/attic/attic_temp/LWT` (nové) |

Stav: todo

### Detektor kouře chodba

Repo `smoke_det_esp32` → `corridor_smoke`, client id `corridor-smoke`.

| Staré | Nové |
|---|---|
| `house/corridor/stat/smoke` | `stat/house/corridor/smoke_detector/smoke` |
| — | `tele/house/corridor/smoke_detector/LWT` (nové) |

Stav: todo

**Nejdůležitější LWT v celém domě.** Detektor kouře, který přestane vysílat,
vypadá dnes stejně jako detektor, který nic nedetekuje. QoS 1 u poplachu i LWT,
a v HA na LWT navázat notifikaci.

### Teplota bazén

Repo `pool_temperature_esp32` → `pool_sensor`, client id `pool-sensor`.

| Staré | Nové |
|---|---|
| `garden/pool/stat/temp` | `stat/garden/pool/pool_sensor/temp` |
| `garden/pool/stat/batt` | `stat/garden/pool/pool_sensor/batt` |
| `garden/pool/stat/waterlevel` | `stat/garden/pool/pool_sensor/water_level` |
| — | `tele/garden/pool/pool_sensor/LWT` (nové) |

Stav: todo

`waterlevel` → `water_level`. **Zůstává na baterii s dobíjením** (potvrzeno
2026-08-18). Jestli reálně spí (deep sleep), z kódu potvrzené není — pokud ano,
LWT nefunguje smysluplně (odpojení = normální stav) a dostupnost se musí řešit
stářím hodnoty. Zvaž u tohohle jediného modulu **vynechat TLS**: handshake při
každém probuzení stojí výdrž.

## Zařízení bez firmwaru v `Devices`

U těchhle nevím, co je fyzicky publikuje — přejmenování nejde naplánovat,
dokud se to nezjistí (otázka B1).

| Dnešní téma | Navržené nové | Stav |
|---|---|---|
| `house/workroom/stat/{temp,hum}` | `stat/house/workroom/climate_sensor/{temp,hum}` | blokováno B1 |
| `house/workroom/stat/light` | `stat/house/workroom/light_sensor/light` | blokováno B1 |
| `house/workroom/{stat,cmnd}/clock/POWER` | `{stat,cmnd}/house/workroom/clock/POWER` | blokováno B1 |
| `house/workroom/3dprinter/…` (vše) | — | **zrušeno** |

**3D tiskárna se ruší.** Ender s vlastním měřením byl nahrazen **Bambulab P2S**,
která vlastní ESP nepotřebuje. Celá větev `house/workroom/3dprinter/…` zaniká
včetně detektoru kouře u tiskárny. Tím zároveň mizí jediné téma s obráceným
pořadím (jméno před prefixem) — nové schéma tedy nemá výjimku.

Kdyby se P2S někdy měla do HA napojit, půjde to přes vlastní integraci
Bambulabu (LAN mode), ne přes tohle schéma témat.

## 433 MHz čidla

Nemají vlastní téma; chodí kódem do `tele/house/workroom/rf_bridge/RESULT`.
Přejmenování se jich přímo netýká, ale **v HA dostanou vlastní entity**
s vlastními zónami:

| Čidlo | entity_id |
|---|---|
| únik vody kotel půda | `binary_sensor.attic_water_boiler` |
| únik vody koupelna 1. patro | `binary_sensor.bathroom_up_water` |
| únik vody koupelna přízemí | `binary_sensor.bathroom_down_water` |
| únik vody kuchyň | `binary_sensor.kitchen_water` |
| únik vody bazén | `binary_sensor.pool_water` |
| pohyb obývák | `binary_sensor.livroom_motion` |
| pohyb zahrada 1, 2 | `binary_sensor.garden_motion_1`, `_2` |
| dveře garáž 1, 2 | `binary_sensor.garage_door_1`, `_2` |
| dveře zahradní domek | `binary_sensor.garden_house_door` |
| ovladač alarmu 1–3 | `event.alarm_remote_1` … `_3` |

Kódy jsou v `secrets/`, ne tady. Zóna `bathroom_up` / `bathroom_down` je nová —
zavést i jako oblast v HA.

**433 MHz zůstává** (rozhodnuto 2026-08-18); Zigbee je až budoucí úvaha. Bridge
je proto dál jediný bod selhání pro alarm i pro vodu — dej mu LWT s navázanou
notifikací, ať je aspoň vidět, když umře.

## Kontrola po dokončení

Až budou všechny řádky výše `v HA`, mělo by platit:

```
mosquitto_sub -t '#' -v          # nesmí být nic mimo cmnd/ stat/ tele/ homeassistant/ sonoffs/
mosquitto_sub -t 'tele/+/+/+/LWT' -v   # každé zařízení právě jednou, Online
```

Každé téma musí mít **pět úrovní**. Cokoli kratšího nebo delšího je zbytek
starého schématu.
