@echo off
rem ============================================================================
rem  KURZY CNB - NANECISTO
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\stocks-tracker\scripts\update_rates.py
rem   Jen vypis, do sesitu nic nezapisuje.
rem ============================================================================
echo.
echo ============================================================
echo   KURZY CNB - NANECISTO
echo ============================================================
echo.
call "%~dp0_run.bat" update_rates.py
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
