@echo off
rem ============================================================================
rem  ZALOHA KONFIGURACI - GoodSync, Total Commander, Thunderbird
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\backups\scripts\backup_configs.py
rem   Zapisuje do D:\Work\Backup\. Nejdriv zkus zaloha_konfiguraci_nanecisto.bat.
rem ============================================================================
echo.
echo ============================================================
echo   ZALOHA KONFIGURACI - GoodSync, Total Commander, Thunderbird
echo ============================================================
echo.
call "%~dp0_run.bat" backup_configs.py 
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
