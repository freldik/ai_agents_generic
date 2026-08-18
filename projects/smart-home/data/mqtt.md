# MQTT (dnešní stav)

> Zdroj: OpenHAB `conf/things/mqtt.things` + `.ino` soubory v `Devices` (stav 2026-08-13).
> Témata jsou tedy **ověřená v kódu zařízení**, ne odhad. Co je z nich dnes živé
> v Home Assistantu, ověřeno není — viz [migrace](migrace.md).
>
> ⚠️ **Schéma témat se při reflashi mění.** Cílový tvar je
> `<prefix>/<lokalita>/<zona>/<zarizeni>/<vec>` — viz
> [konvence_nova](konvence_nova.md). Co se na co převádí, je
> v [prejmenovani](prejmenovani.md). Soupis níže platí pro zařízení,
> která ještě nejsou přeflashovaná.

## Broker

| | |
|---|---|
| Software | Mosquitto, **add-on v Home Assistantu** (ne samostatná služba) |
| Host | **`192.168.5.22`**, port `1883` |
| TLS | dnes ne; **plánuje se zapnout při reflashi** |
| Autentizace | ano, uživatel + heslo — **údaje v `secrets/`** |

Je **jeden broker**. `192.168.0.52` i `192.168.0.106` ve starých configech jsou
neplatné adresy z doby před přečíslováním sítě — nešlo o dva brokery.

⚠️ **Zařízení se starým firmwarem se dnes k brokeru nepřipojí.** Adresa v jejich
konfiguraci neexistuje. Soupis témat níže je proto popis **schématu**, ne
důkaz, že po něm dnes něco chodí.

Broker byl s HAOS **nainstalovaný znovu**, takže v něm nezůstala retained
témata po OpenHABu ani po vyřazených modulech — začíná se od prázdného.

## Struktura témat

Kořen není jeden — jsou **tři podle lokality**:

```
house/<mistnost>/…      dům            (workroom, livroom, kitchen, bedroom, attic, corridor)
around/<misto>/…        kolem domu     (garage, balcony)
garden/…                zahrada        (+ garden/house/…, garden/pool/…)
```

Za lokalitou následuje prefix a jméno zařízení (Tasmota `FullTopic` je
`<lokalita>/%prefix%/%topic%/`):

| Prefix | Směr | Co |
|---|---|---|
| `cmnd` | do zařízení | příkaz |
| `stat` | ze zařízení | stav |
| `tele` | ze zařízení | telemetrie (INFO1–3, STATE, RESULT) |

Vlastní ESP moduly drží stejné schéma, ale mají prefix až za lokalitou i tam, kde
Tasmota má jméno zařízení (např. `garden/pool/stat/temp` — bez jména zařízení).
Jediná výjimka s obráceným pořadím byla 3D tiskárna
(`house/workroom/3dprinter/stat/power`) — ta je zrušená, viz níže.

## Soupis témat

### Dům — pracovna (`house/workroom/`)

| Téma | Směr | Payload | Zařízení |
|---|---|---|---|
| `stat/switch/POWER` / `cmnd/switch/POWER` | out/in | ON/OFF | Tasmota světlo |
| `stat/socket/POWER` / `cmnd/socket/POWER` | out/in | ON/OFF | Tasmota zásuvka |
| `tele/rfbridge/RESULT` | out | JSON `.RfReceived.Data` | RF bridge |
| `stat/temp`, `stat/hum` | out | číslo | čidlo teplota/vlhkost |
| `stat/light` | out | číslo | čidlo světla |
| `stat/clock/POWER` / `cmnd/clock/POWER` | out/in | ON/OFF, **retained** | hodiny |
| ~~`3dprinter/…`~~ | — | — | **zrušeno** — vlastní měření na Enderu, tiskárna už neexistuje |

3D tiskárna (Ender s vlastním měřením) byla nahrazena **Bambulab P2S**, která
vlastní ESP nepotřebuje. Celá větev `house/workroom/3dprinter/…` je mrtvá.
Pokud se P2S bude někdy integrovat, půjde to přes vlastní integraci Bambulabu
v HA, ne přes tohle schéma témat.

### Dům — ostatní

| Téma | Payload | Co |
|---|---|---|
| `house/livroom/{stat,cmnd}/socket/POWER` | ON/OFF | zásuvka obývák |
| `house/livroom/{stat,cmnd}/socket2/POWER` | ON/OFF | vánoční světla komín |
| `house/livroom/{stat,cmnd}/wall_touch/POWER1` | ON/OFF | světlo terasa dveře |
| `house/livroom/{stat,cmnd}/wall_touch/POWER2` | ON/OFF | vypínač terasa |
| `house/kitchen/{stat,cmnd}/socket/POWER` | ON/OFF | zásuvka kuchyň |
| `house/bedroom/{stat,cmnd}/socket/POWER` | ON/OFF | zásuvka ložnice |
| `house/attic/stat/temp` | číslo | teplota půda |
| `house/corridor/stat/smoke` | `ON` | detektor kouře chodba |

### Kolem domu (`around/`)

| Téma | Payload | Co |
|---|---|---|
| `around/garage/stat/air/temp` | číslo | teplota vzduch garáž |
| `around/garage/stat/wardrobe/temp` | číslo | teplota skříň |
| `around/garage/stat/wardrobe/tempset` / `cmnd/…` | číslo, **retained** | žádaná teplota skříně |
| `around/garage/{stat,cmnd}/heat_switch/heat` | ON/OFF | topení skříň |
| `around/garage/{stat,cmnd}/wall_touch/POWER1` | ON/OFF | světlo garáž |
| `around/garage/{stat,cmnd}/wall_touch/POWER2` | ON/OFF | sloupy terasa |
| `around/balcony/{stat,cmnd}/light_switch/POWER` | ON/OFF | vánoční světla balkon |

### Zahrada (`garden/`)

| Téma | Payload | Co |
|---|---|---|
| `garden/{stat,cmnd}/light_switch1/POWER` | ON/OFF | světlo terasa zeď 1 |
| `garden/{stat,cmnd}/light_switch2/POWER` | ON/OFF | světlo terasa zeď 2 |
| `garden/stat/temp` | číslo | teplota zahrada |
| `garden/stat/light` | číslo | čidlo světla zahrada |
| `garden/house/{stat,cmnd}/light_out/POWER` | ON/OFF | venkovní světlo domku |
| `garden/house/{stat,cmnd}/light_switch/POWER` | ON/OFF | vánoční světla domku |
| `garden/house/stat/temp` | číslo | teplota domek |
| `garden/house/{stat,cmnd}/clock/POWER` | ON/OFF, **retained** | hodiny domek |
| `garden/house/cmnd/clock/value` | string | text na displej hodin |
| `garden/pool/stat/temp` | číslo | teplota bazén |
| `garden/pool/stat/batt` | číslo (V) | baterie čidla bazén |
| `garden/pool/stat/waterlevel` | číslo | hladina bazén |

### Telemetrie Tasmota (u všech Sonoffů)

`<lokalita>/tele/<topic>/INFO1` (Version, Module), `INFO2` (Hostname, IPAddress),
`INFO3` (RestartReason), `STATE` (Uptime, `Wifi.RSSI`) — vše JSON.

## Pravidla

- Payload je **prostá hodnota** (`ON`/`OFF`, číslo), ne JSON. JSON má jen
  Tasmota telemetrie a `RfReceived`.
- `retained` je explicitně jen u tří témat: obojí `clock/POWER` a
  `wardrobe/tempset` — tj. tam, kde stav musí přežít restart.
- Vlastní moduly **nemají LWT**. Výpadek se poznával až pravidly „sensor check“
  v OpenHABu podle stáří poslední hodnoty.
- Skupinové téma Tasmoty: `sonoffs` (`MQTT_GRPTOPIC`) — hromadný příkaz všem.

## Entity v Home Assistantu

Dnes jsou zařízení v HA **definovaná ručně**, ne přes MQTT discovery. Pro
cílový stav se to má obrátit — discovery u Tasmot i u vlastních modulů, viz
[konvence_nova](konvence_nova.md). Každá ručně psaná entita je místo, kde se
dokumentace rozejde s realitou.

## Otevřené otázky

- Které z těchhle témat dnes reálně někdo publikuje? (otázka B1 — modul po
  modulu označit běží / neběží / vyhozeno)
- Které ruční `mqtt:` entity v HA dnes existují? Bez konfigurace HA se to
  nedá ověřit.
