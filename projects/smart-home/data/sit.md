# Síť

> Zdroj: OpenHAB záloha a `Devices` (stav 2026-08-13), doplněno odpověďmi
> uživatele 2026-08-18. Údaje o routeru a rozsazích jsou zatím hrubé — Mikrotik
> nebyl pročtený. **Hesla a klíče sem nepatří** — patří do `secrets/`.

## Segment

Dnes jedna plochá síť, **`192.168.5.0/24`** (odvozeno z adresy HA `192.168.5.22`;
maska ověřená není). Rozdělení je jen přes SSID, žádná VLAN dnes neběží.

> ⚠️ **Adresy `192.168.0.x` ve firmwaru jsou mrtvé.** Všechny konfigurace
> v `Devices` míří na `192.168.0.52` / `.106` — to je stav před přečíslováním
> sítě. Dnes je broker na `192.168.5.22`. Znamená to, že **žádné staré zařízení
> se dnes nepřipojí k brokeru, dokud se nepřeflashuje** — což je zároveň důvod,
> proč se reflash stejně dělá.

Cílem je segmentace do VLAN, viz [Segmentace](#segmentace--rozhodnuto) níže.

## Router a brána

| | |
|---|---|
| Model | **Mikrotik** (konkrétní model doplnit) |
| IP brány | `192.168.5.1` ? — odvozeno z rozsahu, neověřeno |
| DHCP | **Mikrotik** |
| DNS | ? — pravděpodobně taky Mikrotik |
| Podpora VLAN | ano (Mikrotik) — počítá se s ní, viz níže |
| Správa | Winbox / web / SSH |

Mikrotik umí VLAN i firewall pravidla po zařízeních, takže plán oddělení
kamer i IoT je proveditelný bez výměny hardwaru.

### Přístupové body

Tři AP s vlastními SSID (viz níže). **Kde která fyzicky je, není zjištěno** —
otázka C2 (uživatel doplní později). U zahradních zařízení a kamer to rozhoduje
o pokrytí.

Cílový stav: k VLAN pro smart home (a případně pro kamery) budou **samostatné
routery s vlastní Wi-Fi sítí**, ne jen další SSID na stávajících AP.

## Adresace

Dnešní stav:

| Skupina | Jak |
|---|---|
| Většina zařízení (ESP, Sonoffy, telefony) | **dynamicky z DHCP** |
| Kamery | **staticky** |
| Home Assistant / broker | `192.168.5.22` |

Návrh pro reflash — rozsahy v rámci `192.168.5.0/24`:

| Rozsah | K čemu |
|---|---|
| `.1` | router (Mikrotik) |
| `.2`–`.49` | infrastruktura: AP, switch, server s HA + brokerem |
| `.50`–`.99` | rezervace pro IoT (Sonoffy, vlastní ESP) |
| `.100`–`.149` | rezervace pro kamery |
| `.150`–`.254` | DHCP pool pro telefony, notebooky, návštěvy |

`192.168.5.22` (HA + broker) do rozsahu infrastruktury sedí, není důvod
ho stěhovat.

**Rezervace podle MAC, ne statická IP v zařízení.** Rezervace se dá změnit
z jednoho místa v routeru; statická adresa natvrdo v ESP znamená reflash.
U kamer, kde je dnes statická adresa nastavená v kameře, ať je adresa
**zároveň v rezervacích** — jinak ji router může přidělit někomu jinému.

Až vzniknou VLAN, dostane každá vlastní podsíť a rozsahy výše se rozpadnou
podle nich; do té doby platí jako plán pro jednu síť.

## Wi-Fi SSID

| SSID | Kde se používá | Zařízení |
|---|---|---|
| `freldik_ntw` | dům | teplota půda, detektor kouře chodba, smart hodiny (druhá varianta buildu) |
| `freldik_ntw_liv` | obývák / garáž | topení skříň garáž |
| `freldik_ntw_garden` | zahrada | temp+light modul, teplota bazén, smart hodiny |

Jde o tři AP se samostatnými SSID, ne o roaming pod jedním jménem —
firmware má SSID natvrdo, takže **přejmenování SSID znamená reflashnout moduly**.

**`_liv` je zavádějící jméno** — používá ho topení skříně v garáži, ne obývák.

> Dřívější doporučení „SSID nepřejmenovávat" **padá**. Vzniká samostatná
> smart-home VLAN s vlastní Wi-Fi, takže moduly nové SSID dostanou tak jako tak.

Cíl pro novou smart-home síť: **jedno SSID s roamingem** na všech AP (stejné
jméno i heslo), ne tři jména podle umístění. ESP modul se pak sám přepne
k silnějšímu AP a odpadne řešení, které zařízení patří kam — což je přesně
ta věc, kterou dnes musí řešit tabulka výše.

Jméno volit tak, aby nešlo zaměnit s domácí sítí, a **hlavně definitivně** —
je ve firmwaru natvrdo. Heslo do `secrets/`.

## Známé adresy

| Adresa | Co to je | Jistota |
|---|---|---|
| `192.168.5.22` | **Raspberry Pi s HAOS** — Home Assistant + Mosquitto add-on | vysoká (od uživatele) |
| `192.168.0.52` | broker ve starých configech a ve všech vlastních ESP | **neplatné** — stav před přečíslováním |
| `192.168.0.106` | `MQTT_HOST` v části Tasmota configů | **neplatné** — starší adresa téhož brokeru, druhý broker nikdy neběžel |
| `192.168.0.105`, `.109`, `.113`, `.120` | v `ip.txt` u některých Sonoffů jako `http://…/cn` | nízká — spíš adresa v době konfigurace, ne rezervace; otázka C4 |

Adresy Sonoffů se nedokumentovaly staticky; každý hlásil svou IP telemetrií
`tele/<topic>/INFO2` (`IPAddress`) a OpenHAB ji jen zobrazoval.

## Servery a služby

Home Assistant běží na **stejném Raspberry Pi jako dřív OpenHAB**, ale je
přeinstalované na **HAOS** (Home Assistant Operating System) — ne HA v Dockeru
nebo v Pythonu na Raspbianu. Mosquitto na něm běží jako **add-on**, ne jako
samostatná služba, takže adresa brokeru je vždy adresa HA.

| Služba | Host | Port | Poznámka |
|---|---|---|---|
| Home Assistant (HAOS) | `192.168.5.22` | 8123 | jádro systému; verze doplnit |
| Mosquitto (add-on v HA) | `192.168.5.22` | 1883 | jeden broker, s heslem, dnes bez TLS |
| Home Assistant Cloud (Nabu Casa) | — | — | **placené**, používá se na vzdálený přístup a zálohy |
| OpenHAB | — | — | **zrušeno**, neběží |
| openHAB Cloud | myopenhab.org | — | **účet zrušen** |

**Ven do internetu není vystavené nic** — žádný port forward ani reverse proxy.
Vzdálený přístup jde přes HA Cloud, který se připojuje odchozím spojením.

Broker běží jako add-on, což má dva důsledky pro reflash: adresa brokeru
je adresa HA a **restart HA znamená restart brokeru** (proto retained LWT,
viz [konvence_nova](konvence_nova.md)).

## Kamery

Šest kamer (obývák, garáž, před domem, terasa, zahrada 2×), značky **Reolink**
a **TP-Link Tapo**. Připojené **přes Wi-Fi**, ne po LAN — tedy žádné PoE
a u zahradních kusů je limitem pokrytí, ne kabel. Nahrávají **na SD karty
uvnitř kamer**, nikam jinam. Adresy jsou **statické** (nastavené v kameře);
konkrétní hodnoty doplnit. Pojmenování a doporučení jsou v [kamery](kamery.md).

| Kamera | Jméno | IP | Poznámka |
|---|---|---|---|
| obývák | `cam-livroom` | ? | značka doplnit (Reolink / Tapo) |
| garáž | `cam-garage` | ? | |
| před domem | `cam-front` | ? | |
| terasa | `cam-terrace` | ? | |
| zahrada 1 | `cam-garden-north` | ? | jméno podle směru ověřit |
| zahrada 2 | `cam-garden-south` | ? | jméno podle směru ověřit |

Statické adresy zapsat i jako **DHCP rezervace v Mikrotiku** — jinak je router
může přidělit jinému zařízení a vznikne konflikt.

## Segmentace — rozhodnuto

Uživatel se 2026-08-18 rozhodl pro VLAN. Tím padá dřívější doporučení
„IoT neoddělovat" — cena reflashe se platí tak jako tak.

| Skupina | Cíl |
|---|---|
| **Smart home (ESP, Sonoffy)** | **vlastní VLAN** s vlastním routerem a Wi-Fi sítí |
| **Kamery** | **vlastní VLAN** (případně tatáž jako smart home, ale spíš zvlášť), bez přístupu do internetu |
| **Domácí síť** | telefony, notebooky, návštěvy — oddělené od obojího |

Protože je **SSID ve firmwaru natvrdo**, musí se jméno a heslo nové smart-home
Wi-Fi znát **dřív, než se začne flashovat**. Rozhodnout SSID → postavit VLAN →
teprve pak flashovat. Opačné pořadí znamená flashovat dvakrát.

Pořadí prací: definovat VLAN a SSID → kamerám zakázat WAN → TLS na brokeru →
DHCP rezervace → reflash zařízení do nové sítě.

## Otevřené otázky

- Jaký konkrétní Mikrotik a jaké má rozsahy DHCP poolu? Dělá i DNS?
- Ověřit masku sítě — `192.168.5.0/24` je odvozeno z jedné adresy.
- **Jaké SSID a heslo bude mít smart-home VLAN?** Blokuje reflash (viz výše).
- Kde která ze tří AP fyzicky je (otázka C2)? Rozhoduje o pokrytí zahrady.
- Co znamenají adresy `192.168.0.105/109/113/120` v `ip.txt` (otázka C4)?
- IP adresy a modely jednotlivých kamer.
