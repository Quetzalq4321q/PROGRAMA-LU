@echo off
chcp 65001 > nul
title Analizador de Descomposición LU

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Ocurrió un problema al ejecutar el programa.
    pause
)
