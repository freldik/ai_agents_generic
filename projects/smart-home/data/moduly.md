# Moduly

> Zdroj: `D:\Electronics\Smart House\Devices` (stav k 2026-08-13) a MQTT témata
> z poslední zálohy OpenHABu. Sloupec „HA“ = ověřeno, že to dnes jede pod
> Home Assistantem — **zatím nevyplněno u nikoho**, viz [migrace](migrace.md).

Dvě rodiny zařízení:

- **Tasmota** — hotové Sonoffy přeflashované Tasmotou, konfigurace ve
  `Config files/my_user_config.h`, témata podle `MQTT_FULLTOPIC`.
- **Vlastní ESP** — vlastní firmware v Arduinu, každý má svůj git repozitář
  (GitLab `home-proj/automation`), témata natvrdo v `.ino`.

## Tasmota zařízení (Sonoff)

| Zařízení               | Složka                               | HW modul                 | MQTT prefix (FullTopic) | %topic%         | Ovládá                                     |
| ---------------------- | ------------------------------------ | ------------------------ | ----------------------- | --------------- | ------------------------------------------ |
| Světlo pracovna        | `House/Work room/Light switch`       | ? (v configu nevyplněno) | `house/workroom/`       | `switch`        | světlo pracovna                            |
| Zásuvka pracovna       | `House/Work room/Socket`             | SONOFF_S2X               | `house/workroom/`       | `socket`        | zásuvka                                    |
| RF bridge              | `House/Work room/Rf bridge`          | SONOFF_BRIDGE            | `house/workroom/`       | `rfbridge`      | příjem 433 MHz čidel                       |
| Zásuvka obývák         | `House/Living room/Socket`           | SONOFF_S2X               | `house/livroom/`        | `socket`        | zásuvka                                    |
| Zásuvka obývák 2       | `House/Living room/Socket 2`         | SONOFF_S2X               | `house/livroom/`        | `socket2`       | vánoční světla komín                       |
| Nástěnný dotyk obývák  | `House/Living room/Wall touch`       | SONOFF_T12               | `house/livroom/`        | `wall_touch`    | POWER1 světlo terasa dveře, POWER2 vypínač |
| Zásuvka kuchyň         | `House/Kitchen/Socket`               | SONOFF_S2X               | `house/kitchen/`        | `socket`        | zásuvka                                    |
| Zásuvka ložnice        | `House/Bed room/Socket`              | SONOFF_S2X               | `house/bedroom/`        | `socket`        | zásuvka                                    |
| Nástěnný dotyk garáž   | `Garage/Wall touch`                  | SONOFF_T12               | `around/garage/`        | `wall_touch`    | POWER1 světlo garáž, POWER2 sloupy terasa  |
| Vánoční balkon         | `Balcony/Christmas switch`           | SONOFF_BASIC             | `around/balcony/`       | `light_switch`  | vánoční světla balkon                      |
| Světlo terasa zeď 1    | `Terrace/Terrace light main switch1` | ?                        | `garden/`               | `light_switch1` | světlo terasa zeď 1                        |
| Světlo terasa zeď 2    | `Terrace/Terrace light main switch2` | ?                        | `garden/`               | `light_switch2` | světlo terasa zeď 2                        |
| Světlo zahradní domek  | `Garden house/Light switch`          | ?                        | `garden/house/`         | `light_out`     | venkovní světlo domku                      |
| Vánoční zahradní domek | `Garden house/Christmas switch`      | SONOFF_BASIC             | `garden/house/`         | `light_switch`  | vánoční světla domku                       |

`%topic%` není v `my_user_config.h` — je nastaven v konfiguraci konkrétního kusu.
Hodnoty výše jsou odvozené z OpenHAB things, kde se skutečná témata používají.

**`MQTT_HOST` v configech (`192.168.0.52` i `.106`) je neplatný** — broker je dnes
na `192.168.5.22`. Obě staré adresy patřily témuž brokeru, druhý nikdy neběžel.
Viz [sit](sit.md).

**Verze Tasmoty:** zařízení byla nedávno aktualizovaná, ale konkrétní verze
u jednotlivých kusů zapsaná není. Odkaz na `thehackbox.org/tasmota/release/sonoff.bin`
v configu je dávno mrtvý. Při reflashi se všude nahraje **nejnovější Tasmota**
a verze se doplní sem.

## Vlastní ESP moduly

| Modul | Složka / repo | Deska | Wi-Fi SSID | MQTT client id | Publikuje | Odebírá |
|---|---|---|---|---|---|---|
| Topení skříň garáž | `Garage/Wardrobe heater` → `wardrobe_heater` | ESP-07 (ESP8266) | `freldik_ntw_liv` | `ESP8266ClientWardrobeHeater` | `around/garage/stat/wardrobe/temp`, `.../air/temp`, `.../wardrobe/tempset`, `around/garage/stat/heat_switch/heat` | `around/garage/cmnd/wardrobe/tempset` |
| Teplota + světlo zahr. domek | `Garden house/Temp light module` → `temp_light_module` | ESP-07 (ESP8266) | `freldik_ntw_garden` | `ESP8266ClientTempLightModule` | `garden/house/stat/temp`, `garden/stat/temp`, `garden/stat/light` | — |
| Smart hodiny zahr. domek | `Garden house/Smart clock` → `smart_clock` | ESP32-WROOM (DOIT DEVKIT V1) | `freldik_ntw_garden` / `freldik_ntw` | `ESP8266ClientSmartClock` / `...House` | — (jen displej) | `garden/stat/temp`, `garden/pool/stat/temp`, `garden/stat/light`, `garden/house/cmnd/clock/value`, `garden/house/cmnd/clock/POWER`, `house/workroom/stat/light`, `house/workroom/cmnd/clock/POWER` |
| Teplota půda | `House/Attic/attic_temperature` → `temperature_esp32` | ESP-07 (ESP8266) | `freldik_ntw` | `ESP8266ClientTemp` | `house/attic/stat/temp` | — |
| Detektor kouře chodba | `House/Hall/Smoke sensor` → `smoke_det_esp32` | ESP-07 (ESP8266) | `freldik_ntw` | `ESP8266ClientSmoke` | `house/corridor/stat/smoke` | — |
| Teplota bazén | `Pool/Pool temperature sensor` → `pool_temperature_esp32` | ESP-07 (ESP8266) | `freldik_ntw_garden` | `ESP8266ClientTempPoolModule` | `garden/pool/stat/temp`, `garden/pool/stat/batt`, `garden/pool/stat/waterlevel` | — |

**Deska — potvrzeno uživatelem 2026-08-18:** u většiny modulů je **ESP-07**
(ESP8266), jediné ESP32 jsou smart hodiny s modulem **ESP32-WROOM**. Názvy
repozitářů `*_esp32` jsou tedy u většiny nepravdivé; při reflashi se ruší,
viz [konvence_nova](konvence_nova.md).

ESP-07 má externí anténu — u zahradních modulů je to výhoda, se kterou počítej
při plánování pokrytí nové smart-home Wi-Fi.

**Aktualizace firmwaru:** dnes se flashuje **kabelem**, OTA v kódu vlastních
modulů není. Cíl je **rozchodit OTA všude** — v ESPHome je zadarmo, u vlastních
`.ino` znamená přidat `ArduinoOTA`. Vzhledem k tomu, kde moduly fyzicky jsou
(půda, zahradní domek, bazén), je to hlavní argument pro přepis do ESPHome.

**Zdroj pravdy pro firmware:** část modulů je jen lokálně v `Devices`, část
v GitLabu, a rozešlo se to. Uživatel plánuje srovnat. Do té doby ověřuj obojí
a ber jako platnější to, co je na zařízení.

## Bezdrátová 433 MHz čidla (přes RF bridge)

Nemají vlastní firmware; hlásí se kódem do `house/workroom/tele/rfbridge/RESULT`
a OpenHAB je rozpoznával podle kódu. Kódy jsou v `secrets/`, ne tady.

| Čidlo | Kde | K čemu sloužilo |
|---|---|---|
| únik vody — kotel půda | půda | poplach voda |
| únik vody — koupelna 1. patro | 1. patro | poplach voda |
| únik vody — koupelna přízemí | přízemí | poplach voda |
| únik vody — kuchyň | přízemí | poplach voda |
| únik vody — bazén | zahrada | poplach voda |
| pohyb — obývací pokoj | obývák | alarm |
| pohyb — zahrada 1, 2 | zahrada | alarm, spínání světel |
| dveře — garáž 1, 2 | garáž | alarm, večerní kontrola zavření |
| dveře — zahradní domek | zahrada | alarm, večerní kontrola zavření |
| dálkový ovladač alarmu (3 ks) | — | zapnout/vypnout alarm |

## Zařízení bez složky v `Devices`

Objevují se v OpenHABu, ale nemají adresář s firmwarem — ověřit, co to fyzicky je:

- teplota + vlhkost pracovna (`house/workroom/stat/temp`, `/hum`)
- čidlo světla pracovna (`house/workroom/stat/light`)
- hodiny pracovna (`house/workroom/{stat,cmnd}/clock/POWER`)
- čidlo teploty zahrada (`garden/stat/temp` — publikuje ho temp_light_module)
- hlavní uzávěr vody, siréna alarmu

## Zrušené

| Co | Kdy | Poznámka |
|---|---|---|
| 3D tiskárna Ender + vlastní měření (`house/workroom/3dprinter/…`) | před 2026-08-18 | nahrazeno **Bambulab P2S**, která vlastní ESP nepotřebuje |

S Enderem odpadl i detektor kouře u tiskárny, který byl v OpenHABu svázaný
s detektorem na chodbě — viz [migrace](migrace.md).

## Ostatní zařízení (mimo MQTT)

| Co | Kde | Stav |
|---|---|---|
| Amazon Echo (Alexa) | obývák, ložnice | **používá se** k hlasovému ovládání |
| Bambulab P2S | pracovna | do smart home zatím nenapojená |
| Kamery | 6× | viz [kamery](kamery.md) |

## Otevřené otázky

- Které moduly dnes reálně běží a jsou už v Home Assistantu? (otázka B1)
- Chybějící `MODULE` v configu u 4 kusů (Light switch pracovna, Light switch
  zahradní domek, Terrace switch 1 a 2) — doplnit typ HW. (otázka C1)
- Co fyzicky publikuje teplotu, vlhkost, světlo a hodiny v pracovně?
