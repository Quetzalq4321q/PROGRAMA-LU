@echo off
chcp 65001 > nul
title Demostración Consola - Analizador LU

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py --cli
) else (
    python main.py --cli
)

echo.
echo Presione cualquier tecla para salir...
pause > nul
