# Kamery

> Sepsáno 2026-08-18 podle zadání (6 kamer: obývák, garáž, před domem, terasa,
> zahrada 2×), doplněno odpověďmi téhož dne. Značky jsou známé, **modely,
> rozlišení, RTSP cesty ani IP adresy zatím ne**.
> Konvence níže je návrh, aby se kamery pojmenovaly správně hned napoprvé.

## Dnešní stav

| | |
|---|---|
| Značky | **Reolink** a **TP-Link Tapo** (které je které, doplnit) |
| Připojení | **Wi-Fi**, žádné PoE ani LAN |
| IP | **statické**, nastavené v kameře |
| Záznam | **SD karta uvnitř každé kamery** — žádný NVR, žádný Frigate |
| V Home Assistantu | zatím nic |

Dvě značky znamenají **dvě různé RTSP cesty**. Reolink:
`rtsp://<user>:<heslo>@<ip>:554/h264Preview_01_main` (a `_sub`).
Tapo: `rtsp://<user>:<heslo>@<ip>:554/stream1` (a `stream2`), navíc s vlastním
účtem pro kameru, který se zakládá v aplikaci Tapo — není to účet do cloudu.

**Záznam jen na SD kartě je slabé místo:** kdo kameru odnese nebo zničí, odnese
i záznam. To je zároveň hlavní důvod pro plánovaný NAS s Frigate (viz níže).

## Zásada

Kamera **není MQTT zařízení** — video jde přes RTSP, ne přes broker. Do MQTT
vstupuje až detekce (Frigate publikuje události), a to pod vlastním kořenem,
ne pod `stat/…`. Neohýbat kamery do schématu témat.

Zato platí totéž pravidlo jako u ESP modulů: **jedno jméno na všech místech** —
hostname, DHCP rezervace, klíč ve Frigate/go2rtc, entity_id v HA. Když uvidíš
`cam-front` v routeru, víš okamžitě, co to je.

## Pojmenování

```
cam-<zona>[-<rozliseni>]
```

Zóna je stejná jako v MQTT schématu (viz [konvence_nova](konvence_nova.md)).
Rozlišující přípona jen tam, kde je v jedné zóně kamer víc.

| Kamera | Jméno | Zóna | entity_id | Oblast v HA |
|---|---|---|---|---|
| obývák | `cam-livroom` | `house/livroom` | `camera.livroom` | Obývák |
| garáž | `cam-garage` | `around/garage` | `camera.garage` | Garáž |
| před domem | `cam-front` | `around/front` | `camera.front` | Před domem |
| terasa | `cam-terrace` | `around/terrace` | `camera.terrace` | Terasa |
| zahrada 1 | `cam-garden-north` | `garden/main` | `camera.garden_north` | Zahrada |
| zahrada 2 | `cam-garden-south` | `garden/main` | `camera.garden_south` | Zahrada |

**Zahradní kamery pojmenuj podle směru nebo podle toho, co snímají**
(`-north` / `-south`, nebo `-gate` / `-pool`), **ne `-1` / `-2`**. Za rok
nebudeš vědět, která je která, a při poplachu v notifikaci „pohyb na garden-2“
je číslo k ničemu. Návrh výše je zástupný — uprav podle skutečné orientace
(otázka A4).

`around/front` a `around/terrace` jsou zóny, které kvůli kamerám vznikají —
`terrace` se navíc stěhuje z `garden` do `around`, viz
[prejmenovani](prejmenovani.md).

## Streamy

Většina kamer nabízí dva streamy. Používej oba a nemíchej je:

| Stream | Rozlišení | K čemu |
|---|---|---|
| main / stream0 | plné | nahrávání, přehrávání záznamu |
| sub / stream1 | nízké | detekce, živý náhled v dashboardu |

Detekce na hlavním streamu zbytečně vytíží stroj; náhled v dashboardu na hlavním
streamu zahltí Wi-Fi. Ve Frigate se to nastavuje rolemi `record` / `detect`.

## Entity v HA

Kamera jako HA device má víc než jen obraz. Pojmenování drží konvenci
`<zona>_<vec>`:

```
camera.front                      obraz
binary_sensor.front_motion        pohyb
binary_sensor.front_person        detekce osoby (Frigate)
switch.front_detect               zapnout/vypnout detekci
sensor.front_fps                  diagnostika
```

Zobrazované jméno česky, bez místnosti (tu dodá oblast): `Kamera`, `Pohyb`,
`Osoba`.

## Frigate

**Dnes neběží nikde.** Plán je pořídit **NAS s dostatečným výkonem** a Frigate
provozovat na něm, ne na Raspberry Pi s HAOS — to na detekci objektů u šesti
kamer výkon nemá, a navíc by tím dostal na starost i nahrávání.

Mezistupeň, který jde udělat hned a zadarmo: kamery přidat do HA jako
`generic_camera` přes RTSP (nebo go2rtc, který je v HA už zabudovaný). Dá to
živý obraz v dashboardu a možnost automatizací na pohyb hlášený samotnou
kamerou, bez detekce objektů a bez nároků na výkon. Až bude NAS, přibude Frigate
nad tytéž streamy — pojmenování z toho zůstane platné.

Konfigurace níže platí pro cílový stav s Frigate.

Klíč kamery ve `frigate.yml` **musí být totožný s hostname** — Frigate z něj
odvozuje jména entit i MQTT témat, a rozejít se to nesmí:

```yaml
cameras:
  cam_front:          # podtržítko: Frigate nepovolí pomlčku v klíči
    ffmpeg:
      inputs:
        - path: rtsp://<user>:<heslo>@192.168.5.X:554/<cesta>
          roles: [record]
        - path: rtsp://<user>:<heslo>@192.168.5.X:554/<cesta_sub>
          roles: [detect]
```

Frigate je jediné místo, kde se od konvence odchýlíme na podtržítko
(`cam_front` místo `cam-front`) — je to jeho omezení, ne volba.

MQTT témata Frigate publikuje pod vlastním kořenem `frigate/…`. Ten nechat, jak
je, a **nepřevádět do schématu `stat/…`** — je to samostatná integrace se svou
konvencí, kterou HA umí číst nativně.

Heslo ke kamerám patří do `secrets/`, ne sem a ne do `frigate.yml` v gitu.

## Síť

Kamery jdou do **vlastní VLAN** (rozhodnuto 2026-08-18, viz [sit](sit.md)).
Na rozdíl od ESP modulů je přesun levný — kamera se dá přendat do jiné sítě
bez zásahu do firmwaru.

Platí i uvnitř VLAN:

- **Statická IP** je už nastavená; zapsat ji navíc jako **DHCP rezervaci**
  v Mikrotiku, aby ji router nepřidělil někomu jinému.
- **Blokovat kamerám přístup do internetu.** Reolink i Tapo volají domů;
  do HA se dostanou po LAN a víc nepotřebují. Cena: přijdeš o mobilní aplikaci
  přes cloud a o firmware update jedním klikem — updaty se pak dělají ručně.
- **Vypnout na kamerách cloud, P2P a UPnP.** UPnP si umí otevřít port ven samo,
  i když jsi žádný port forward nedělal.
- Vlastní účet pro Frigate/HA, jen ke čtení streamu, ne admin.
- **Wi-Fi kamery zatíží síť.** Šest kamer na Wi-Fi je hlavní argument pro to,
  aby smart-home moduly a kamery **nebyly na stejné rádiové síti** — ESP modul
  s krátkým paketem jednou za minutu nemá soupeřit s trvalým video streamem.

Adresy doplnit do [sit](sit.md), až budou známé.

## Otevřené otázky

- Které konkrétní kamery jsou Reolink a které Tapo? Modely a rozlišení?
  Bez modelu nedohledám RTSP cestu.
- Zahrada 1/2 — kam skutečně míří, ať se dají pojmenovat popisně (otázka A4).
- Jak dlouhou historii držet, až bude NAS? Určuje kapacitu disku.
- Má kamera v obýváku běžet pořád, nebo jen když nikdo není doma? V HA se to
  dělá vypnutím streamu, ne jen skrytím z dashboardu.
