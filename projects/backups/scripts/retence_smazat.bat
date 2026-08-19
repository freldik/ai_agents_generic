@echo off
rem ============================================================================
rem  RETENCE RAR ARCHIVU - MAZANI
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\retention.py --delete
rem   POZOR: maze soubory. Skript se jeste zepta na potvrzeni.
rem ============================================================================
echo.
echo ============================================================
echo   RETENCE RAR ARCHIVU - MAZANI
echo ============================================================
echo.
call "%~dp0_run.bat" retention.py --delete
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
