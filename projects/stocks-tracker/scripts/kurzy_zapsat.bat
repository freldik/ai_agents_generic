@echo off
rem ============================================================================
rem  KURZY CNB - ZAPIS DO SESITU
rem  Spusteni: dvojklik na tenhle soubor.
rem  Odpovida: .venv\Scripts\python.exe projects\stocks-tracker\scripts\update_rates.py --write
rem   ZAPISUJE kurzy do oblasti Kurzy v sporeni.xlsx.
rem ============================================================================
echo.
echo ============================================================
echo   KURZY CNB - ZAPIS DO SESITU
echo ============================================================
echo.
echo   Zapise do D:\Work\Finance\Test\sporeni.xlsx (predtim udela sporeni.bak.xlsx).
echo   Sesit musi byt v Excelu ZAVRENY.
echo   Zrusit: zavri okno nebo Ctrl+C. Pokracovat: libovolna klavesa.
echo.
pause
echo.
call "%~dp0_run.bat" update_rates.py --write
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
