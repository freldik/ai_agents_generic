@echo off
rem ============================================================================
rem  Spolecny spoustec pro python skripty tohoto projektu.
rem  Nevolej primo - volaji ho male .bat obalky vedle (sync_nanecisto.bat, ...).
rem
rem  Pouziti:  call _run.bat <nazev_skriptu.py> [dalsi parametry]
rem  Vraci navratovy kod python skriptu.
rem ============================================================================
setlocal
if "%~1"=="" (
    echo [CHYBA] _run.bat ocekava nazev skriptu jako prvni parametr.
    exit /b 2
)

rem python vypisuje cesky v UTF-8
chcp 65001 >nul

set "S=%~dp0"
rem repo root = o tri urovne vys nez scripts\  (projects\stocks-tracker\scripts)
for %%i in ("%~dp0..\..\..") do set "REPO=%%~fi"
set "PY=%REPO%\.venv\Scripts\python.exe"

if not exist "%PY%" (
    echo.
    echo [CHYBA] Nenalezeno: %PY%
    echo         Venv neexistuje. Viz CLAUDE.md v koreni repa:
    echo             python -m venv .venv
    echo             .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    exit /b 1
)
if not exist "%S%%~1" (
    echo [CHYBA] Skript neexistuje: %S%%~1
    exit /b 1
)

set "SKRIPT=%~1"
shift
rem slozeni zbylych parametru (shift nefunguje na %*)
set "ARGS="
:sber
if "%~1"=="" goto :spust
set "ARGS=%ARGS% "%~1""
shift
goto :sber

:spust
rem spousti se z korene repa, aby sedely relativni cesty v skriptech
cd /d "%REPO%"
"%PY%" "%S%%SKRIPT%"%ARGS%
exit /b %errorlevel%
