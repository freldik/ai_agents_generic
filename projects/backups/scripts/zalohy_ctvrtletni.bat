@echo off
chcp 65001 >nul

rem ============================================================================
rem  Ctvrtletni zaloha - VSECHNO NAJEDNOU, spousti se RUCNE.
rem
rem  V Planovaci uloh Windows neni naplanovane nic. Zamerne nic nebezi samo:
rem  vsechno je videt na obrazovce a da se to kdykoli zastavit pres Ctrl+C.
rem
rem  Doporucene terminy: leden, duben, cervenec, rijen.
rem
rem  Spusteni: dvojklik, nebo z prikazove radky
rem      projects\backups\scripts\zalohy_ctvrtletni.bat
rem
rem  POZOR: krok 3 (RAR archivace) trva HODINY. Poust to vecer.
rem  NIC v tomhle skriptu nemaze zalohy. Krok 5 jen vypisuje, co je nad
rem  ramec retence - mazani se vzdy spousti zvlast a rucne.
rem ============================================================================

cd /d "%~dp0..\..\.."
set "REPO=%CD%"
set "PY=%REPO%\.venv\Scripts\python.exe"
set "S=%REPO%\projects\backups\scripts"
set "LOGDIR=D:\Work\Backup\Data\_log"
set "CHYBY=0"

for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "DNES=%%d"
set "LOG=%LOGDIR%\zalohy_%DNES%.log"

echo.
echo ============================================================
echo   CTVRTLETNI ZALOHA - %DNES%
echo ============================================================

rem --- Kontrola prostredi pred cimkoli jinym --------------------------------
if not exist "%PY%" (
    echo.
    echo [CHYBA] Nenalezeno: %PY%
    echo         Venv neexistuje. Viz CLAUDE.md v koreni repa.
    goto :konec
)
if not exist "D:\Work\Backup\" (
    echo.
    echo [CHYBA] Neexistuje D:\Work\Backup\ - je pripojeny disk D: ?
    goto :konec
)
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
echo === Ctvrtletni zaloha %DNES% === > "%LOG%"

echo.
echo   Probehne po sobe, bez dalsiho ptani:
echo     1. stav pred zalohou      jen cte
echo     2. zaloha konfiguraci     GoodSync, Total Commander, Thunderbird
echo     3. RAR archivace dat      D:\Others a D:\Projects - TRVA HODINY
echo     4. dokumentace GoodSync   jen cte
echo     5. retence - vypis        NIC NEMAZE
echo     6. stav po zaloze         zapise report do temp\
echo.
echo   Log behu: %LOG%
echo.
echo   Zastavit muzes kdykoli pres Ctrl+C.
echo.
pause

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [1/6] STAV PRED ZALOHOU - co je po terminu
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [1/6] status.py >> "%LOG%"
"%PY%" "%S%\status.py"
if errorlevel 1 (
    echo   [CHYBA] status.py skoncil chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK]
    echo     OK >> "%LOG%"
)

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [2/6] ZALOHA KONFIGURACI - GoodSync, Total Commander, Thunderbird
echo        jen nastaveni, par vterin; posta samotna se nezalohuje
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [2/6] backup_configs.py >> "%LOG%"
"%PY%" "%S%\backup_configs.py"
if errorlevel 1 (
    echo   [CHYBA] backup_configs.py skoncil chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK]
    echo     OK >> "%LOG%"
)

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [3/6] RAR ARCHIVACE DAT - D:\Others a D:\Projects
echo        TRVA HODINY a zabere desitky GB. Nech okno bezet.
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [3/6] backup_data.bat >> "%LOG%"
call "%S%\backup_data.bat"
if errorlevel 1 (
    echo   [CHYBA] RAR archivace skoncila chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK] RAR archivace dokoncena
    echo     OK >> "%LOG%"
)

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [4/6] DOKUMENTACE GOODSYNC JOBU - precte jobs.tic
echo        jen cte, jobs.tic se nikdy needituje
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [4/6] goodsync_jobs.py >> "%LOG%"
"%PY%" "%S%\goodsync_jobs.py"
if errorlevel 1 (
    echo   [CHYBA] goodsync_jobs.py skoncil chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK]
    echo     OK >> "%LOG%"
)

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [5/6] RETENCE RAR ARCHIVU - jen vypis, NIC SE NEMAZE
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [5/6] retention.py >> "%LOG%"
"%PY%" "%S%\retention.py" --out "%LOGDIR%\retence_report.md"
if errorlevel 1 (
    echo   [CHYBA] retention.py skoncil chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK]
    echo     OK >> "%LOG%"
)
echo.
echo   ^> Kdyz chces stare archivy opravdu smazat, spust zvlast a potvrd:
echo     .venv\Scripts\python.exe projects\backups\scripts\retention.py --delete

rem =========================================================================
echo.
echo ------------------------------------------------------------
echo  [6/6] STAV PO ZALOZE - zapise report do projects\backups\temp\
echo ------------------------------------------------------------
echo. >> "%LOG%"
echo --- [6/6] status.py --md >> "%LOG%"
"%PY%" "%S%\status.py" --md
if errorlevel 1 (
    echo   [CHYBA] status.py skoncil chybou
    echo     CHYBA >> "%LOG%"
    set /a CHYBY+=1
) else (
    echo   [OK]
    echo     OK >> "%LOG%"
)

rem =========================================================================
echo.
echo ============================================================
if "%CHYBY%"=="0" (
    echo   HOTOVO - vsech 6 kroku probehlo bez chyby
) else (
    echo   HOTOVO - ale %CHYBY% krok/y skoncil/y chybou, viz vypis vyse
)
echo ============================================================
echo.
echo   Rucni kroky, ktere skript neumi - vsechno pres webove rozhrani:
echo     - Home Assistant  ... snapshot
echo     - routery         ... export konfigurace
echo     - WD MyCloud      ... kontrola stavu disku
echo     - Thunderbird     ... export posty obou uctu
echo     - Todoist         ... export upominek a ukolu
echo   Podrobnosti: projects\backups\data\inventory.md
echo.
echo   Log: %LOG%

:konec
echo.
pause
exit /b
