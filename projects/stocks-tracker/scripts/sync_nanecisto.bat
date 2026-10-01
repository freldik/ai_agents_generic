@echo off
rem ============================================================================
rem  AKCIE Z XTB - NANECISTO
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\stocks-tracker\scripts\xtb_sync.py --dry-run
rem   Jen vypis a report do data\, do sesitu nic nezapisuje.
rem ============================================================================
echo.
echo ============================================================
echo   AKCIE Z XTB - NANECISTO
echo ============================================================
echo.
call "%~dp0_run.bat" xtb_sync.py --dry-run
set "RC=%errorlevel%"
echo.
if "%RC%"=="0" (
    echo [OK] Hotovo.
) else (
    echo [CHYBA] Skript skoncil s kodem %RC%.
)
echo.
pause
exit /b %RC%
