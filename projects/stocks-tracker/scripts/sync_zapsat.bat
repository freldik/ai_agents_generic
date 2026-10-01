@echo off
rem ============================================================================
rem  AKCIE Z XTB - ZAPIS DO SESITU
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\stocks-tracker\scripts\xtb_sync.py --write
rem   ZAPISUJE Investovano a Hodnota do sporeni.xlsx. Nejdriv pust sync_nanecisto.bat.
rem ============================================================================
echo.
echo ============================================================
echo   AKCIE Z XTB - ZAPIS DO SESITU
echo ============================================================
echo.
echo   Zapise do D:\Work\Finance\Test\sporeni.xlsx (predtim udela sporeni.bak.xlsx).
echo   Sesit musi byt v Excelu ZAVRENY.
echo   Zrusit: zavri okno nebo Ctrl+C. Pokracovat: libovolna klavesa.
echo.
pause
echo.
call "%~dp0_run.bat" xtb_sync.py --write
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
