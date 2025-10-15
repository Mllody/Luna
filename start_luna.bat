@echo off
title Agent LUNA - Backend Starter
cd /d C:\LUNA
echo Uruchamianie środowiska LUNA...
call venv\Scripts\activate
echo [LUNA] Aktywacja środowiska OK
echo [LUNA] Start backendu Flask...
python backend\app.py
pause
