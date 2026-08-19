@echo off
rem ============================================================================
rem  STAV ZALOH + ulozeni reportu do data\
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\status.py --md
rem   Zapise data\status_YYYY-MM-DD.md, jinak nic nemeni.
rem ============================================================================
echo.
echo ============================================================
echo   STAV ZALOH + ulozeni reportu do data\
echo ============================================================
echo.
call "%~dp0_run.bat" status.py --md
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
