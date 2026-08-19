@echo off
rem ============================================================================
rem  STAV ZALOH - co je po terminu
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\status.py
rem   Jen cte, nic nezapisuje.
rem ============================================================================
echo.
echo ============================================================
echo   STAV ZALOH - co je po terminu
echo ============================================================
echo.
call "%~dp0_run.bat" status.py 
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
