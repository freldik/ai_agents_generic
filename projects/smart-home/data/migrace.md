# Migrace OpenHAB → Home Assistant

> Zdroj: `D:\Electronics\Smart House\OpenHab\Last backup` (záloha z 2025-04-21,
> zapsáno 2026-08-13). OpenHAB **neběží**; tohle je seznam funkcí, které v něm byly,
> jako zadání pro Home Assistant.

## Pravidla

- Co je v OpenHABu a **není** v HA → stav `nepřeneseno`. Nepatří to do
  [moduly](moduly.md) ani [mqtt](mqtt.md) jako živá věc.
- Co je přenesené a ověřené → stav `hotovo (YYYY-MM-DD)`.
- Co se vědomě nepřenáší → `zahozeno` a **důvod**, ať se to neotvírá znovu.

## Stav položek

Stavy: `nepřeneseno` / `rozpracováno` / `hotovo (YYYY-MM-DD)` / `zahozeno`.
Vše je zatím `nepřeneseno` — skutečný stav HA nebyl ověřen.

### Alarm (`rules/alarm.rules`, 568 řádků — nejsložitější část)

| Funkce | Stav |
|---|---|
| zapnutí/vypnutí alarmu 433 MHz ovladačem (3 ovladače) | nepřeneseno |
| kontrola „vše zavřeno“ před aktivací, potvrzení blikáním světel | nepřeneseno |
| pohybová čidla obývák + zahrada 1/2, timeout pohybu 30 s | nepřeneseno |
| dveřní čidla garáž 1/2, zahradní domek (OPEN/CLOSE) | nepřeneseno |
| poplach: světla na 300 s, siréna na 60 s | **částečně odloženo** — světla ano, siréna není ovládaná |

### Světla (`rules/lights.rules`)

| Funkce | Stav |
|---|---|
| dvojklik / vypnutí na nástěnném dotyku → světla terasa zeď a sloupy | nepřeneseno |
| světlo zahrada podle soumraku (astro sunrise/sunset + čidlo světla) | nepřeneseno |
| světlo garáž 1/2 na čidlo pohybu | nepřeneseno |
| ovládání zahradních světel dálkovým ovladačem | nepřeneseno |
| vánoční světla: režimy „vždy zapnuto“ / „jen když jsme doma“ | nepřeneseno |

### Poruchy a bezpečnost

| Funkce | Stav |
|---|---|
| únik vody — 5 čidel (kotel půda, koupelna 1. p., koupelna přízemí, kuchyň, bazén) | nepřeneseno |
| po úniku vody zavřít hlavní uzávěr vody | **odloženo** — uzávěr není fyzicky ovládaný, viz níže |
| detektor kouře chodba, opakovaná notifikace | nepřeneseno |
| ~~detektor kouře u 3D tiskárny~~ | **zahozeno** — Ender nahrazen Bambulab P2S, čidlo zaniklo |
| ruční reset poruchy (voda / požár) | nepřeneseno |

### Ostatní automatiky (`rules/others.rules`)

| Funkce | Stav |
|---|---|
| večerní kontrola zavření garáže 1/2 a zahradního domku | nepřeneseno |
| hodiny zahradní domek / pracovna — ranní zapnutí, večerní vypnutí, text času | nepřeneseno |
| nabíjení baterie čidla bazénu | nepřeneseno — čidlo **zůstává** na baterii s dobíjením |
| topení skříně v garáži na žádanou teplotu (`tempset`) | nepřeneseno |
| automatický reboot serveru, restart/vypnutí z UI | nepřeneseno |

### Hlídání čidel (`rules/sensor_check.rules`, `last_update.rules`)

| Funkce | Stav |
|---|---|
| u každého čidla čas poslední hodnoty + perioda hlášení | nepřeneseno |
| souhrnný stav „všechna čidla OK“, kontrola zapínatelná | nepřeneseno |

V HA to řeší `last_changed` a šablonové senzory dostupnosti — nejspíš půjde
udělat mnohem jednodušeji než těch 156 řádků pravidel.

### Integrace

| Funkce | Stav |
|---|---|
| Amazon Echo (hlasové ovládání) | nepřeneseno — **Alexa se používá dál** (obývák, ložnice), integrace do HA chybí |
| astro (východ/západ slunce) | nepřeneseno — v HA je `sun` zabudovaný |
| systeminfo Raspberry Pi (CPU, paměť, disk, teplota) | nepřeneseno — v HA integrace „System Monitor“ |
| openHAB Cloud (vzdálený přístup) | **zahozeno** — účet zrušen, nahrazeno placeným HA Cloud |
| persistence rrd4j + mapdb (historie a přežití restartu) | nepřeneseno — v HA recorder |
| sitemap `house.sitemap` (594 řádků UI) | zahodit — HA má vlastní dashboardy |

### Notifikace

**Notifikuje se do aplikace Home Assistant** (`notify.mobile_app_*`), ne
e-mailem ani Telegramem. Všechna pravidla, která v OpenHABu posílala zprávu
přes openHAB Cloud, se přepisují na tohle.

U poplachů (kouř, únik vody, alarm) nastav notifikaci jako **kritickou**
(`push.sound.critical` na iOS, kanál s vysokou prioritou na Androidu) — jinak
ji ztiší režim Nerušit, což je přesně ta situace, kdy na ní záleží nejvíc.

## Co si z OpenHABu odnést

- **Struktura místností** v `items/g*.items` (přízemí, 1. patro, půda, garáž,
  balkon, terasa, zahrada, zahradní domek, bazén) se dá 1:1 použít jako
  oblasti v HA.
- Každý Sonoff měl kromě spínače i 6 diagnostických položek (název, modul,
  verze, IP, restart, uptime, RSSI). V HA je většina z toho zadarmo přes
  Tasmota discovery — nepřepisovat ručně.

## Rozhodnutí (2026-08-18)

- **433 MHz přes RF bridge zůstává.** Zigbee je možná budoucnost, ale ne teď —
  alarm i únik vody se přenášejí tak, jak jsou. Bridge tím pádem zůstává
  jediným bodem selhání pro obojí; při reflashi mu dej **LWT s notifikací**,
  ať je aspoň vidět, když umře.
- **Siréna a hlavní uzávěr vody nikdy nebyly implementované** — v OpenHABu
  byly jen jako položky bez MQTT kanálu, takže je fyzicky neovládalo nic.
  Řeší se později, jako nová instalace, ne jako migrace.
- **Notifikace jde do HA app.**
- **Zálohy:** HA Cloud zálohuje do cloudu automaticky, uživatel si je
  **jednou měsíčně stahuje k sobě**. Tenhle ruční krok o sobě projekt `backups`
  zatím neví — patří tam.

## Otevřené otázky

- Co už v HA reálně je? Do ověření je celá tabulka jen odhad (otázka B3).
- Ověřit, že se měsíční stahování zálohy HA opravdu děje — u ručního kroku
  se to pozná až ve chvíli, kdy je záloha potřeba.
