@echo off
rem ============================================================================
rem  RETENCE RAR ARCHIVU - JEN VYPIS
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\retention.py
rem   NIC NEMAZE. Jen ukaze, co je nad ramec 4+1/rok.
rem ============================================================================
echo.
echo ============================================================
echo   RETENCE RAR ARCHIVU - JEN VYPIS
echo ============================================================
echo.
call "%~dp0_run.bat" retention.py 
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
