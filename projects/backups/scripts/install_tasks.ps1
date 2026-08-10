# Naplanuje zalohovaci skripty do Planovace uloh Windows.
#
# Vsechny ulohy bezi pod prihlasenym uzivatelem (ne jako SYSTEM) — potrebuji
# pristup k namapovanym jednotkam a k %APPDATA%. Kdyz pocitac v dany cas nebezi,
# uloha se spusti pri nejblizsim startu (/Z ... StartWhenAvailable).
#
# Pouziti:
#   powershell -ExecutionPolicy Bypass -File projects\backups\scripts\install_tasks.ps1
#   ... -Install     opravdu vytvori ulohy
#   ... -Uninstall   ulohy zase smaze

param(
    [switch]$Install,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$repo    = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$python  = Join-Path $repo '.venv\Scripts\python.exe'
$scripts = Join-Path $repo 'projects\backups\scripts'
$logs    = 'D:\Work\Backup\Data\_log'

# Kazda uloha: nazev, popis, co spustit, kdy (argumenty pro schtasks).
$tasks = @(
    @{
        Name     = 'Zalohy - RAR archivy'
        Desc     = 'WinRAR archivace D:\Others a D:\Projects. Ctvrtletne, trva hodiny. Zamerne az 2. — 1. je rucni synchronizacni vecer.'
        Command  = "`"$scripts\backup_data.bat`""
        Schedule = @('/SC', 'MONTHLY', '/M', 'JAN,APR,JUL,OCT', '/D', '2', '/ST', '20:00')
    },
    @{
        Name     = 'Zalohy - konfigurace'
        Desc     = 'GoodSync, Total Commander, nastaveni Thunderbirdu. Mesicne, par vterin.'
        Command  = "`"$python`" `"$scripts\backup_configs.py`""
        Schedule = @('/SC', 'MONTHLY', '/D', '1', '/ST', '20:30')
    },
    @{
        Name     = 'Zalohy - kontrola stavu'
        Desc     = 'Report co je po terminu. Tydne, jen cte.'
        Command  = "`"$python`" `"$scripts\status.py`" --md"
        Schedule = @('/SC', 'WEEKLY', '/D', 'MON', '/ST', '18:00')
    },
    @{
        Name     = 'Zalohy - retence (jen report)'
        Desc     = 'Vypise, ktere RAR archivy jsou nad ramec 4+1/rok. NEMAZE. Az 3., aby videl i archiv z predchoziho dne.'
        Command  = "`"$python`" `"$scripts\retention.py`" --out `"$logs\retence_report.md`""
        Schedule = @('/SC', 'MONTHLY', '/D', '3', '/ST', '20:00')
    },
    @{
        Name     = 'Zalohy - seznam GoodSync jobu'
        Desc     = 'Prepise dokumentaci jobu z jobs.tic. Jen cte.'
        Command  = "`"$python`" `"$scripts\goodsync_jobs.py`""
        Schedule = @('/SC', 'MONTHLY', '/D', '1', '/ST', '20:35')
    }
)

if (-not (Test-Path $python)) {
    Write-Host "CHYBA: nenalezeno $python" -ForegroundColor Red
    exit 1
}

if ($Uninstall) {
    foreach ($t in $tasks) {
        Write-Host "Mazu: $($t.Name)"
        schtasks /Delete /TN "$($t.Name)" /F
    }
    exit 0
}

foreach ($t in $tasks) {
    $args = @('/Create', '/TN', $t.Name, '/TR', $t.Command) + $t.Schedule +
            @('/RL', 'LIMITED', '/Z', '/V1', '/F')
    if ($Install) {
        Write-Host "Vytvarim: $($t.Name)" -ForegroundColor Green
        & schtasks @args
    } else {
        Write-Host "`n$($t.Name)" -ForegroundColor Cyan
        Write-Host "  $($t.Desc)"
        Write-Host "  schtasks $($args -join ' ')" -ForegroundColor DarkGray
    }
}

if (-not $Install) {
    Write-Host "`nNic se nevytvorilo. Opravdove vytvoreni: -Install" -ForegroundColor Yellow
}
