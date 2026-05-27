@echo off
cd /d "%~dp0"

set PORTA=8765
set URL=http://127.0.0.1:%PORTA%

REM Abre o navegador automaticamente.
start "" "%URL%"

REM Inicia o servidor local.
python server.py
pause
