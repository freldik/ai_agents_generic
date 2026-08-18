# Cílová konvence (po reflashi)

> Navrženo 2026-08-18 pro přechod OpenHAB → Home Assistant, kdy se **přeflashují
> všechna zařízení**. **Schéma témat i přesun terasy do `around` uživatel
> potvrdil 2026-08-18** — je to tedy závazný cíl, ne návrh k diskusi.
> Tenhle dokument popisuje **cílový stav**, ne dnešní realitu.
> Dnešní realita je v [konvence](konvence.md) a [mqtt](mqtt.md).
> Převod staré téma → nové je v [prejmenovani](prejmenovani.md).

Dokud není přeflashováno všechno, platí obojí a je nutné vědět, které zařízení je
v jakém stavu — sloupec „stav“ v [prejmenovani](prejmenovani.md).

## Proč se schéma mění

Staré schéma `<lokalita>/<prefix>/<zarizeni>/<vec>` má dvě vady, které se projeví
až v Home Assistantu:

1. **Prefix je uprostřed cesty.** Nejde odebírat podle směru — neexistuje
   wildcard „všechny stavy“ ani „všechny příkazy“.
2. **Lokalita má proměnnou hloubku** (`garden` = 1 úroveň, `house/workroom` = 2,
   `garden/pool` = 2). Tím se rozbije každý wildcard, i kdyby prefix seděl.

Obojí je oprava, která stojí jen přepsání jednoho řetězce ve firmwaru. Když se
stejně flashuje, je to zadarmo; později už ne.

## MQTT téma

```
<prefix>/<lokalita>/<zona>/<zarizeni>/<vec>
```

Pět úrovní, **vždy pět**, u každého zařízení bez výjimky. Prefix vepředu,
lokalita a zóna vždy dvě samostatné úrovně.

```
stat/house/workroom/ceiling_light/POWER
cmnd/house/workroom/ceiling_light/POWER
tele/house/workroom/rf_bridge/LWT
stat/garden/pool/pool_sensor/temp
cmnd/around/garage/wardrobe_heater/tempset
```

### prefix

| Prefix | Směr | Co |
|---|---|---|
| `cmnd` | do zařízení | příkaz |
| `stat` | ze zařízení | stav (odpověď na příkaz, hodnota čidla) |
| `tele` | ze zařízení | telemetrie, diagnostika, `LWT` |

Díky prefixu vepředu fungují tyhle odběry, které dřív nešly:

```
stat/#                     všechny stavy v domě
cmnd/#                     všechny příkazy (ladění: kdo co posílá)
stat/garden/+/+/+          všechno na zahradě
tele/+/+/+/LWT             dostupnost všech zařízení naráz
```

### lokalita a zóna

Lokalita je vždy jedna ze tří, zóna je vždy uvedená — i tam, kde je jen jedna.
`garden` samo o sobě už neexistuje, je z něj `garden/main`.

| Lokalita | Zóny |
|---|---|
| `house` | `workroom`, `livroom`, `kitchen`, `bedroom`, `attic`, `corridor`, `bathroom_up`, `bathroom_down` |
| `around` | `garage`, `balcony`, `terrace`, `front` |
| `garden` | `main`, `house`, `pool` |

Změny proti dnešku:

- **`terrace` je nová zóna pod `around`**, ne pod `garden`. Terasa je fyzicky
  u domu; zařazení k zahradě bylo historické a mátlo.
- **`front`** (před domem) je nová zóna — zatím jen pro kameru.
- **`bathroom_up` / `bathroom_down`** jsou nové zóny pro čidla úniku vody,
  která dnes nemají vlastní téma (chodí přes RF bridge).
- `garden` → `garden/main`.

Zóna = **oblast v Home Assistantu**, jedna ku jedné. Když přidáváš zónu sem,
přidej ji i jako area v HA.

### zařízení

Jméno zařízení je **funkce, ne hardware**. `wall_touch` říká, že je to dotykový
panel — to je informace, která zestárne s výměnou kusu. `ceiling_light` říká,
co to dělá, a to platí dál.

Snake_case, malými písmeny, bez diakritiky, bez čísel na konci tam, kde jde
použít slovo.

| Místo | Nově | Proč |
|---|---|---|
| `switch` (pracovna) | `ceiling_light` | „switch“ neříká nic |
| `socket2` (obývák) | `xmas_chimney` | číslo neříká, co je na zásuvce |
| `light_switch1/2` (terasa) | `wall_light_l` / `wall_light_r` | totéž |
| `light_switch` (balkon) | `xmas_balcony` | sjednoceno s ostatními vánočními |
| `light_switch` (domek) | `xmas_garden_house` | totéž |
| `light_out` (domek) | `outdoor_light` | |
| `heat_switch` (garáž) | součást `wardrobe_heater` | jeden modul = jedno zařízení |
| `wardrobe` (garáž) | součást `wardrobe_heater` | totéž |

**Dvoukanálové Sonoffy** (`wall_touch`) jsou jediné, kde funkční jméno nejde —
jeden kus má jeden `%topic%` a dva kanály, které svítí na dvě různá místa.
Řešení: `%topic%` pojmenovat podle **umístění panelu**, a rozlišení funkce nechat
až na entity v HA.

```
stat/house/livroom/switch_panel/POWER1     světlo terasa dveře
stat/house/livroom/switch_panel/POWER2     vypínač terasa
stat/around/garage/switch_panel/POWER1     světlo garáž
stat/around/garage/switch_panel/POWER2     sloupy terasa
```

Z tématu tedy pořád nepoznáš funkci — ale poznáš ji z entity v HA, kde jméno
nastavuješ ručně (viz níže). To je správné místo, kde tu informaci držet.

### věc

Poslední úroveň. Tasmota kanály velkými (`POWER`, `POWER1`, `POWER2`) — to je
dané Tasmotou, nesjednocovat. Vlastní věci malými:

`temp`, `hum`, `light`, `smoke`, `batt`, `water_level`, `tempset`, `heat`,
`value`, `LWT`, `STATE`, `INFO1`–`3`, `RESULT`

Sjednoceno: `waterlevel` → `water_level`.

## Payload

Beze změny — je to udělané dobře:

- Prostá hodnota (`ON` / `OFF`, číslo). **Ne JSON.**
- JSON jen tam, kde ho vnucuje Tasmota (`STATE`, `INFO*`, `RESULT`).
- Čísla bez jednotky, jednotka patří do definice entity v HA.
- Desetinná tečka, ne čárka.

## Retain

Retained je **jen** téma, jehož hodnota musí přežít restart brokeru i zařízení:

| Téma | Proč retained |
|---|---|
| `cmnd/around/garage/wardrobe_heater/tempset` | žádaná teplota — po restartu se nesmí ztratit |
| `cmnd/+/+/clock/POWER` | zapnutí hodin |
| `tele/+/+/+/LWT` | dostupnost — HA musí vidět stav i po svém restartu |

**Hodnoty čidel retained nejsou.** Retained teplota vypadá po restartu jako
čerstvá hodnota z mrtvého čidla — přesně to, čemu se snažíme zabránit.

## LWT — dostupnost

**Nově povinné u každého zařízení**, včetně vlastních modulů. Dnes ho nemá žádný
vlastní modul a výpadek se pozná až podle stáří hodnoty; u detektoru kouře je to
nebezpečné.

```
tele/<lokalita>/<zona>/<zarizeni>/LWT
```

Payload `Online` / `Offline`, **retained, QoS 1** — přesně jako Tasmota, aby šla
v HA použít jedna a tatáž konfigurace pro obě rodiny zařízení.

V kódu vlastního modulu:

```cpp
// will je součást connect(), ne samostatné publish
client.connect(clientId, mqttUser, mqttPass,
               "tele/house/attic/attic_sensor/LWT", 1, true, "Offline");
client.publish("tele/house/attic/attic_sensor/LWT", "Online", true);
```

V ESPHome to dělá `mqtt:` komponenta sama — jen nastavit `birth_message` /
`will_message` na stejné téma a payload.

## QoS

- `0` — hodnoty čidel, které chodí periodicky. Ztráta jedné nevadí, přijde další.
- `1` — příkazy (`cmnd/#`), `LWT`, poplachy (`smoke`, únik vody), `tempset`.
- `2` — nepoužívat. Režie navíc, přínos u ničeho z tohohle nulový.

## Skupinové téma

Tasmota `MQTT_GRPTOPIC` = `sonoffs`. Ponechat, ale **nepoužívat v automatizacích** —
hromadný příkaz všem Sonoffům včetně vánočních světel a zásuvky s mrazákem není
nic, co bys chtěl spustit omylem. Je to nástroj pro údržbu (restart, OTA).

## Client id / hostname

```
<zona>-<zarizeni>
```

Malými, pomlčky (ESPHome nepovolí podtržítko v `name`), stejné jako MQTT client id
i jako hostname i jako jméno ESPHome node. Jedno jméno na všech třech místech —
když ho uvidíš v routeru, hned víš, co to je.

```
attic-sensor
garage-wardrobe-heater
pool-sensor
workroom-rf-bridge
garden-house-clock
```

Ruší se `ESP8266Client<Název>` — deska v client id nemá co dělat (a byla stejně
u poloviny modulů uvedená špatně).

## Home Assistant

### Oblasti

Oblast = zóna z MQTT tématu, jedna ku jedné. Česky, s diakritikou — oblast se jen
zobrazuje, do entity_id nevstupuje.

`Pracovna`, `Obývák`, `Kuchyň`, `Ložnice`, `Půda`, `Chodba`, `Koupelna nahoře`,
`Koupelna dole`, `Garáž`, `Balkon`, `Terasa`, `Před domem`, `Zahrada`,
`Zahradní domek`, `Bazén`

### Zařízení (device)

Jedno fyzické zařízení = jedno HA device, i když má víc entit. Jméno česky,
podle funkce a místa: `Topení skříně garáž`, `Čidlo bazén`, `Dotyk obývák`.

U MQTT discovery se device skládá z bloku `device` (`identifiers`, `name`,
`manufacturer`, `model`, `sw_version`) — vyplnit **vždy**, jinak entity visí
v HA bez zařazení a nejdou hromadně přiřadit do oblasti.

### entity_id

```
<domain>.<zona>_<zarizeni>_<vec>
```

Anglicky, bez diakritiky, snake_case — kopíruje MQTT téma bez lokality a prefixu.
Lokalita se vynechává, protože zóny jsou unikátní napříč celým domem.

```
light.workroom_ceiling_light
switch.livroom_xmas_chimney
sensor.pool_sensor_temp
sensor.pool_sensor_batt
binary_sensor.corridor_smoke_detector
climate.garage_wardrobe_heater
camera.front
```

Když je `<vec>` u zařízení jediná a zřejmá, vynech ji: `light.terrace_wall_light_l`,
ne `light.terrace_wall_light_l_power`.

**Nespoléhej na to, co si HA odvodí z názvu.** Nastav `object_id` v MQTT discovery
(nebo `id:` v ESPHome) explicitně — jinak dostaneš `light.svetlo_pracovna_2`
a už to nikdy nesrovnáš.

### Zobrazované jméno (friendly name)

Česky, s diakritikou, **bez názvu místnosti** — místnost dodá oblast a HA ji
v UI zobrazuje sama. `Stropní světlo`, ne `Světlo pracovna`.

Tady se také narovnává dvoukanálový dotyk: entita
`light.livroom_switch_panel_2` dostane jméno `Terasa u dveří`, ačkoli téma
říká jen `switch_panel/POWER2`.

### Konvence z OpenHABu

`g<Zkratka>_<Věc>_<Atribut>` (`gAHG_Wardrobe_Temperature_Setpoint`) se
**nepřebírá**. HA má oblasti a zařízení; prefixy pro seskupení jsou zbytečné.

### MQTT discovery vs. ruční entity

- **Tasmota** — použít nativní Tasmota discovery (`SetOption19 0` +
  `SetOption73 1` pro tlačítka). Zadarmo z toho přijde i diagnostika (RSSI, uptime,
  IP, verze), kterou jsi v OpenHABu psal ručně jako 6 položek na zařízení.
- **Vlastní ESP** — publikovat discovery zprávu z firmwaru do
  `homeassistant/<component>/<node_id>/<object_id>/config`, retained. Je to pár
  řádků navíc v `setup()` a ušetří to udržování YAML na dvou místech.
- **Ruční `mqtt:` v YAML** — jen tam, kde discovery nejde. Každá ručně psaná
  entita je místo, kde se dokumentace rozejde s realitou.

Do každé discovery zprávy patří `availability_topic` s LWT — bez toho je LWT
k ničemu.

> **Změna proti dnešku.** Dnes jsou entity v HA definované **ručně**. Cílem je
> discovery — u Tasmot je zadarmo (stačí `SetOption19 0`), u vlastních modulů
> je to pár řádků v `setup()` nebo v ESPHome nic. Ruční definice znamená
> udržovat tytéž informace na dvou místech; při reflashi všech zařízení je to
> nejlevnější okamžik, kdy s tím přestat.

## TLS na brokeru

Zapíná se při reflashi (rozhodnuto 2026-08-18). Dnes jde heslo po Wi-Fi
otevřeně.

Pořadí je důležité: **certifikát musí existovat dřív, než se flashuje první
zařízení**, jinak se flashuje dvakrát.

- Mosquitto add-on umí TLS přes `certfile` / `keyfile` v konfiguraci add-onu.
- Vlastní CA je pro domácí síť v pořádku; certifikát pak musí mít v SAN
  **IP adresu** `192.168.5.22`, ne jen hostname — ESP se připojuje na IP.
- Port se mění `1883` → `8883`. Nech obojí otevřené, dokud neběží všechno
  na TLS, jinak si při migraci zamkneš zbytek zařízení venku.
- Na ESP8266 (`WiFiClientSecure`) TLS stojí paměť a čas připojení. U ESP-07
  to projde, ale ověřuj CA otiskem, ne celým řetězcem.
- V ESPHome: `mqtt: certificate_authority: !secret ca_cert`.

**Pozor u modulů na baterii** (čidlo bazén): TLS handshake při každém probuzení
znatelně zkrátí výdrž. Tam zvaž ponechání nešifrovaného spojení, nebo ho
přesuň na nativní API ESPHome, kde je šifrování levnější.

## ESPHome

Nové moduly stavěj v ESPHome, ne v holém Arduinu. Odpadne ruční MQTT, LWT,
OTA i discovery. Vlastní `.ino` má smysl už jen tam, kde ESPHome nestačí.

**Rozhodnuto 2026-08-18:** co půjde, přepsat do ESPHome; zbytek zůstane
s vlastním kódem. Dělicí čára podle dnešních modulů:

| Modul | Cíl | Proč |
|---|---|---|
| Teplota půda | ESPHome | jedno čidlo, nic vlastního |
| Detektor kouře chodba | ESPHome | binární vstup |
| Teplota + světlo zahr. domek | ESPHome | dvě čidla |
| Teplota bazén | ESPHome | + `deep_sleep` komponenta řeší i baterii |
| Topení skříň garáž | ESPHome | `climate` platforma umí termostat nativně |
| Smart hodiny | **vlastní kód** | vlastní logika displeje, odebírá cizí témata |

U modulů, které jdou do ESPHome, tím **automaticky padá otázka OTA i LWT** —
obojí je součástí ESPHome. To je zároveň odpověď na to, jak dostat OTA
na moduly na půdě a u bazénu, aniž bys k nim lezl s kabelem.

**Hodiny zůstávají jediné, kde se musí LWT, OTA i discovery dopsat ručně.**
OTA přidej přes `ArduinoOTA` hned při prvním reflashi — modul v zahradním
domku není místo, kam chceš chodit s notebookem.

### Jméno node

```yaml
esphome:
  name: garage-wardrobe-heater        # = hostname = MQTT client id
  friendly_name: Topení skříně garáž  # tohle HA použije jako jméno device
```

`name` musí sedět s konvencí `<zona>-<zarizeni>` výše.

### API, nebo MQTT?

**Nativní API, ne MQTT** — u ESPHome zařízení je MQTT krok navíc, který nic
nepřidává. Šifrované, rychlejší, dostupnost řeší samo.

MQTT u ESPHome zapni jen tehdy, když ta data potřebuje ještě něco jiného než HA
(např. smart hodiny, které si teplotu berou přímo z brokeru). Pak platí stejná
konvence témat i LWT jako u ostatních:

```yaml
mqtt:
  broker: 192.168.5.22
  topic_prefix: stat/garden/pool/pool_sensor
  birth_message:
    topic: tele/garden/pool/pool_sensor/LWT
    payload: Online
  will_message:
    topic: tele/garden/pool/pool_sensor/LWT
    payload: Offline
```

### entity_id v ESPHome

`friendly_name` na node + krátké `name` na entitě dá `sensor.pool_sensor_temp`
automaticky. Kde to nevychází, přebij `id:`.

```yaml
sensor:
  - platform: dallas_temp
    name: Teplota vody      # zobrazované jméno
    id: pool_sensor_temp    # řídí entity_id
```

### Tajné údaje

Wi-Fi heslo, API klíč a OTA heslo **vždy přes `!secret`**, nikdy natvrdo v YAML.
`secrets.yaml` patří mimo git — v tomhle repu do `secrets/`.

## Kamery

Viz [kamery](kamery.md).

## Git repozitáře firmwaru

GitLab `home-proj/automation/<nazev>`, snake_case, **podle funkce a místa, ne
podle desky**:

```
garage_wardrobe_heater
garden_house_temp_light
garden_house_clock
attic_temp
corridor_smoke
pool_sensor
```

Ruší se sufix `_esp32`, který byl u většiny repozitářů fakticky nepravdivý.
Skutečná deska patří do `device.txt` v repozitáři, kde se dá opravit, aniž by
se přejmenovávalo repo.

## Co se vědomě nemění

- **Payload jako prostá hodnota** — funguje, není důvod na JSON.
- **Tři lokality `house` / `around` / `garden`** — dělení je logické a drží.
- **Tasmota `POWER` velkými** — vnucené Tasmotou.
- **Skupinové téma `sonoffs`** — užitečné pro údržbu.
- **433 MHz přes RF bridge** — zůstává, Zigbee je až budoucí úvaha.

## Co se naopak mění proti dřívějšímu doporučení

- **SSID.** Dřív tu stálo, že se přejmenovávat nemá. Padá to: vzniká
  **samostatná smart-home VLAN s vlastní Wi-Fi** (viz [sit](sit.md)), takže
  moduly stejně dostanou nové SSID. Musí být známé **před** flashováním.
- **VLAN pro IoT.** Dřív „neoddělovat“ — teď rozhodnuto oddělit.
