@echo off
rem ============================================================================
rem  PRUZKUM STROJE - disky, jednotky, ulohy
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\discover.py
rem   Jen cte.
rem ============================================================================
echo.
echo ============================================================
echo   PRUZKUM STROJE - disky, jednotky, ulohy
echo ============================================================
echo.
call "%~dp0_run.bat" discover.py 
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
