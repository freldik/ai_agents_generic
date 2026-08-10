# Průzkum stroje — 2026-08-10

> Generuje `scripts/discover.py`. Podklad pro `data/inventory.md`.

## Disky

```
DriveLetter FileSystemLabel DriveType SizeGB FreeGB
----------- --------------- --------- ------ ------
          F                 CD-ROM         0      0
          E                 Removable      0      0
          D                 Fixed       1863  707,2
          C                 Fixed      892,8  306,6
```

## Síťová úložiště

Připojené síťové jednotky:

```
New connections will be remembered.


Status       Local     Remote                    Network

-------------------------------------------------------------------------------
Disconnected L:        \\FRELICHOVA-NTB\Work     Microsoft Windows Network
OK           M:        \\WDMYCLOUD\Marek         Microsoft Windows Network
Disconnected N:        \\FRELICH-NTB\C           Microsoft Windows Network
OK           P:        \\WDMYCLOUD\Public        Microsoft Windows Network
The command completed successfully.
```

## Naplánované úlohy

Naplánované úlohy mimo systémové (tady se pozná, co už běží samo):

```
Adobe Acrobat Update Task                     Ready     09.08.2026 20:00:01
HPCustParticipation HP OfficeJet Pro 8710     Ready     10.08.2026 17:46:01
NvDriverUpdateCheckDaily_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     09.08.2026 12:25:18
NVIDIA GeForce Experience SelfUpdate_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     30.11.1999 0:00:00
NvNodeLauncher_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     07.08.2026 19:32:55
NvProfileUpdaterDaily_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     09.08.2026 12:25:11
NvProfileUpdaterOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     04.08.2026 19:32:55
NvTmMon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     08.08.2026 11:58:33
NvTmRepOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     04.08.2026 19:32:55
NvTmRep_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     09.08.2026 12:25:11
OneDrive Per-Machine Standalone Update Task   Ready     30.11.1999 0:00:00
OneDrive Reporting Task-S-1-5-21-957055817-1690341386-1872925552-1001 Ready     09.08.2026 19:49:01
OneDrive Startup Task-S-1-5-21-957055817-1690341386-1872925552-1001 Ready     04.08.2026 19:40:55
S-1-5-21-957055817-1690341386-1872925552-1001 Disabled  30.11.1999 0:00:00
AppleSoftwareUpdate                           Ready     08.08.2026 21:26:02
AcPowerNotification                           Running   04.08.2026 19:30:54
ArmourySocketServer                           Ready     04.08.2026 19:30:54
ASUS AISuiteIII                               Ready     04.08.2026 19:30:54
ASUS File Transfer Server Launcher            Ready     04.08.2026 19:30:54
Ez Update                                     Running   04.08.2026 19:30:54
NoiseCancelingEngine                          Ready     04.08.2026 19:30:55
P508PowerAgent_sdk                            Ready     04.08.2026 19:30:54
Open Browser                                  Ready     01.06.2018 19:55:48
RunPlatformExperienceHelperOnUnlock           Ready     10.08.2026 17:31:59
RunPlatformExperienceHelper_Daily             Ready     09.08.2026 19:06:13
RunPlatformExperienceHelper_Metrics           Ready     13.07.2026 16:35:45
Printer Health Monitor                        Ready     10.08.2026 17:28:51
Printer Health Monitor Logon                  Ready     04.08.2026 19:53:09
DataSenseLiveTileTask                         Disabled  30.11.1999 0:00:00
SoftLandingCreativeManagementTask             Ready     09.08.2026 17:02:13
SoftLandingDeferralTask-{9976dcb1-4c40-41ff-9170-f70c638b3246} Ready     10.08.2026 17:47:01
SoftLandingTriggerTask-128000000001615609-render-{6a5aac2c-762a-4129-8abf-cd6d94189f02} Disabled  09.08.2026 17:02:14
```

## Kde leží konfigurace zálohovaných nástrojů

| Nástroj | Cesta | Existuje |
|---|---|---|
| GoodSync | `C:\Users\Marek Frelich\AppData\Roaming\GoodSync` | ano |
| GoodSync | `C:\Users\Marek Frelich\AppData\Local\GoodSync` | ne |
| GoodSync | `C:\ProgramData\Siber Systems\GoodSync` | ne |
| Total Commander | `C:\Users\Marek Frelich\AppData\Roaming\GHISLER` | ano |
| Total Commander | `C:\totalcmd` | ne |
| Total Commander | `C:\Program Files\totalcmd` | ano |
| Thunderbird | `C:\Users\Marek Frelich\AppData\Roaming\Thunderbird\Profiles` | ano |
| Home Assistant (lokální kopie záloh) | `C:\Users\Marek Frelich\Downloads` | ano |
| Home Assistant (lokální kopie záloh) | `C:\Users\Marek Frelich\Documents\HomeAssistant` | ne |

## Nalezené existující zálohovací skripty

_nic nenalezeno_

