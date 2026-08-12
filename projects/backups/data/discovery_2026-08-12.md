# Průzkum stroje — 2026-08-12

> Generuje `scripts/discover.py`. Podklad pro `data/inventory.md`.

## Disky

```
DriveLetter FileSystemLabel DriveType SizeGB FreeGB
----------- --------------- --------- ------ ------
          F                 CD-ROM         0      0
          E                 Removable      0      0
          D                 Fixed       1863  705,9
          C                 Fixed      892,8  298,8
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
Adobe Acrobat Update Task                     Ready     12.08.2026 17:31:34
HPCustParticipation HP OfficeJet Pro 8710     Ready     12.08.2026 18:46:01
NvDriverUpdateCheckDaily_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:26:42
NVIDIA GeForce Experience SelfUpdate_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     30.11.1999 0:00:00
NvNodeLauncher_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:21:38
NvProfileUpdaterDaily_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:26:42
NvProfileUpdaterOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:21:38
NvTmMon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 19:21:34
NvTmRepOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:21:38
NvTmRep_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8} Ready     12.08.2026 17:26:42
OneDrive Per-Machine Standalone Update Task   Ready     12.08.2026 17:26:42
OneDrive Reporting Task-S-1-5-21-957055817-1690341386-1872925552-1001 Ready     12.08.2026 18:30:04
OneDrive Startup Task-S-1-5-21-957055817-1690341386-1872925552-1001 Ready     12.08.2026 17:29:34
S-1-5-21-957055817-1690341386-1872925552-1001 Disabled  30.11.1999 0:00:00
AppleSoftwareUpdate                           Ready     08.08.2026 21:26:02
AcPowerNotification                           Running   12.08.2026 17:19:49
ArmourySocketServer                           Ready     12.08.2026 17:19:49
ASUS AISuiteIII                               Ready     12.08.2026 17:19:49
ASUS File Transfer Server Launcher            Ready     12.08.2026 17:19:43
Ez Update                                     Running   12.08.2026 17:19:49
NoiseCancelingEngine                          Ready     12.08.2026 17:19:49
P508PowerAgent_sdk                            Ready     12.08.2026 17:19:34
Open Browser                                  Ready     01.06.2018 19:55:48
RunPlatformExperienceHelperOnUnlock           Ready     12.08.2026 17:19:58
RunPlatformExperienceHelper_Daily             Ready     12.08.2026 18:48:37
RunPlatformExperienceHelper_Metrics           Ready     13.07.2026 16:35:45
Printer Health Monitor                        Ready     12.08.2026 17:26:42
Printer Health Monitor Logon                  Ready     12.08.2026 17:56:15
DataSenseLiveTileTask                         Disabled  30.11.1999 0:00:00
SoftLandingCreativeManagementTask             Ready     12.08.2026 17:26:42
SoftLandingDeferralTask-{45a5db2f-c180-471e-8b3c-ef297dac341d} Ready     12.08.2026 19:41:01
SoftLandingTriggerTask-128000000001615609-render-{6e359060-aeb0-47be-82c7-9071f65ce141} Disabled  12.08.2026 17:26:42
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

