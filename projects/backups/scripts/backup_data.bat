@echo off
setlocal enabledelayedexpansion
REM ============================================================================
REM  Zaloha velkych datovych slozek do RAR archivu.
REM  Nahrazuje puvodni D:\Work\Skripty\backup_data.bat.
REM
REM  Zmeny proti puvodni verzi:
REM    - archivy jdou rovnou do podslozek D:\Work\Backup\Data\<Kategorie>\
REM      (uz se nic nekopiruje rucne)
REM    - datum se bere z PowerShellu, ne z %date% (to zavisi na locale a rozbije se)
REM    - kontroluje navratovy kod WinRARu, nehlasi "Done" kdyz to spadlo
REM    - loguje do D:\Work\Backup\Data\_log\backup_data_YYMMDD.log
REM    - nove archivy neprepisuje: kdyz dnesni existuje, kategorii preskoci
REM
REM  Retenci (mazani starych archivu) tenhle skript NEDELA. Od toho je
REM  scripts/retention.py, ktery se pousti zvlast a defaultne jen ukazuje.
REM ============================================================================

set "WINRAR=C:\Program Files\WinRAR\WinRAR.exe"
set "DEST=D:\Work\Backup\Data"
set "LOGDIR=%DEST%\_log"

REM ---- kategorie: nazev = zdrojova cesta. Pridani dalsi = jeden radek. --------
set "CAT[0]=Others=D:\Others"
set "CAT[1]=Projects=D:\Projects"
set "CAT_COUNT=2"

REM ---- datum YYMMDD nezavisle na nastaveni Windows ---------------------------
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyMMdd"') do set "STAMP=%%i"

if not exist "%WINRAR%" (
    echo CHYBA: WinRAR nenalezen: %WINRAR%
    exit /b 1
)
if not exist "%DEST%" (
    echo CHYBA: cil neexistuje: %DEST%  ^(je pripojeny disk D:?^)
    exit /b 1
)
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

set "LOG=%LOGDIR%\backup_data_%STAMP%.log"
set "FAILED=0"
set "SKIPPED=0"
set "DONE=0"

echo. >> "%LOG%"
echo ===== %date% %time% ===== >> "%LOG%"

for /l %%n in (0,1,%CAT_COUNT%) do (
    if defined CAT[%%n] (
        for /f "tokens=1,* delims==" %%a in ("!CAT[%%n]!") do (
            set "NAME=%%a"
            set "SRC=%%b"
            set "OUTDIR=%DEST%\!NAME!"
            set "OUT=!OUTDIR!\!NAME!_%STAMP%.rar"

            if not exist "!SRC!" (
                echo [CHYBA] zdroj neexistuje: !SRC!
                echo [CHYBA] zdroj neexistuje: !SRC! >> "%LOG%"
                set /a FAILED+=1
            ) else if exist "!OUT!" (
                echo [preskoceno] dnesni archiv uz existuje: !OUT!
                echo [preskoceno] !OUT! >> "%LOG%"
                set /a SKIPPED+=1
            ) else (
                if not exist "!OUTDIR!" mkdir "!OUTDIR!"
                echo [beh] !NAME!: !SRC! -^> !OUT!
                echo [beh] !NAME! start %time% >> "%LOG%"
                REM -r rekurzivne, -ep1 bez korenove cesty v archivu,
                REM -y potvrdit vse, -ilog zapsat chyby WinRARu do logu
                "%WINRAR%" a -r -ep1 -y -ilog"%LOG%" "!OUT!" "!SRC!\"
                if errorlevel 1 (
                    echo [CHYBA] WinRAR skoncil s kodem !errorlevel! pro !NAME!
                    echo [CHYBA] WinRAR kod !errorlevel! pro !NAME! >> "%LOG%"
                    set /a FAILED+=1
                ) else (
                    echo [ok] !NAME! hotovo
                    echo [ok] !NAME! konec %time% >> "%LOG%"
                    set /a DONE+=1
                )
            )
        )
    )
)

echo.
echo Hotovo: %DONE%   preskoceno: %SKIPPED%   chyb: %FAILED%
echo Souhrn: hotovo=%DONE% preskoceno=%SKIPPED% chyb=%FAILED% >> "%LOG%"
echo Log: %LOG%

if %FAILED% gtr 0 exit /b 1
exit /b 0
