# Konvence pojmenování (dnešní stav)

> Zapsáno podle skutečného stavu (2026-08-13), ne navrženo od stolu.
>
> ⚠️ **Tohle je popis dosluhujícího stavu.** Při přechodu na Home Assistant se
> všechna zařízení přeflashují a platí nová konvence —
> [konvence_nova](konvence_nova.md), převod témat v [prejmenovani](prejmenovani.md).
> Tenhle dokument zůstává, dokud v brokeru mluví starým schématem aspoň jedno
> zařízení; pak se smaže.

## MQTT témata

```
<lokalita>/<prefix>/<zarizeni>/<vec>
```

- **lokalita**: `house/<mistnost>` | `around/<misto>` | `garden` (+ `garden/house`, `garden/pool`)
- **místnosti**: `workroom`, `livroom`, `kitchen`, `bedroom`, `attic`, `corridor`
- **prefix**: `cmnd` (příkaz) | `stat` (stav) | `tele` (telemetrie)
- **zařízení**: `switch`, `socket`, `socket2`, `wall_touch`, `rfbridge`,
  `light_switch`, `light_switch1/2`, `light_out`, `clock`, `heat_switch`, `wardrobe`
- **věc**: `POWER` / `POWER1` / `POWER2` (Tasmota), nebo `temp`, `hum`, `light`,
  `smoke`, `batt`, `waterlevel`, `tempset`

Vše malými písmeny a bez diakritiky; kanál Tasmoty (`POWER`) velkými — to je
dané Tasmotou, nesjednocovat.

Podrobný soupis v [mqtt](mqtt.md).

## Složky zařízení

`Devices/<Lokalita>/<Zařízení>/` — anglicky, s mezerami a velkým prvním písmenem
(`House/Work room/Rf bridge`). Uvnitř Tasmoty: `Config files/`, `Programator/`,
`ip.txt`, `login.txt`. Uvnitř vlastních modulů: `Arduino/` nebo `git/`, `Fotky/`,
`Zapojeni/`, `Schema/`.

## Git repozitáře firmwaru

GitLab `home-proj/automation/<nazev>`, snake_case, sufix podle desky:
`wardrobe_heater`, `smart_clock`, `temp_light_module`, `temperature_esp32`,
`smoke_det_esp32`, `pool_temperature_esp32`.

**Pozor:** sufix `_esp32` u většiny neodpovídá realitě — desky jsou ESP8266.
Nedodržovat to dál; nové repo pojmenovat podle funkce, desku psát do `device.txt`.

## MQTT client id vlastních modulů

`ESP8266Client<NázevModulu>`, např. `ESP8266ClientWardrobeHeater`.

## Wi-Fi SSID

`freldik_ntw` (dům), `freldik_ntw_liv`, `freldik_ntw_garden` — viz [sit](sit.md).

## Položky v OpenHABu (historické)

`g<Zkratka lokality>_<Věc>[_<Atribut>]`, např. `gAHG_Wardrobe_Temperature_Setpoint`
(`AHG` = around house / garage). Popisky česky. V Home Assistantu tuhle konvenci
**nepřebírat** — HA má oblasti a čitelná entity_id.

## Známé výjimky

| Co | Jak se to jmenuje ve skutečnosti | Proč |
|---|---|---|
| světlo terasa dveře, vypínač terasa | pod `house/livroom/wall_touch/…` | fyzicky je vypínač v obýváku, i když svítí na terase |
| sloupy terasa | pod `around/garage/wall_touch/POWER2` | druhý kanál dotyku v garáži |
| světla terasa zeď 1/2 | pod `garden/…`, ne `house/…` | historicky zařazeno k zahradě |
| 3D tiskárna | `house/workroom/3dprinter/stat/…` — jméno **před** prefixem | jediné téma s obráceným pořadím |
| teplota zahrada | publikuje ji modul zahradního domku | jeden modul, dvě čidla |
