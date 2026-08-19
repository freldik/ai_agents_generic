@echo off
rem ============================================================================
rem  ZALOHA KONFIGURACI - NANECISTO (dry-run)
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\backup_configs.py --dry-run
rem   Nic nezapisuje, jen vypise co by delal.
rem ============================================================================
echo.
echo ============================================================
echo   ZALOHA KONFIGURACI - NANECISTO (dry-run)
echo ============================================================
echo.
call "%~dp0_run.bat" backup_configs.py --dry-run
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
