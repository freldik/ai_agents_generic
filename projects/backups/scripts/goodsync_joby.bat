@echo off
rem ============================================================================
rem  DOKUMENTACE GOODSYNC JOBU
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\goodsync_jobs.py
rem   Jen cte jobs.tic, nikdy ho needituje.
rem ============================================================================
echo.
echo ============================================================
echo   DOKUMENTACE GOODSYNC JOBU
echo ============================================================
echo.
call "%~dp0_run.bat" goodsync_jobs.py 
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
