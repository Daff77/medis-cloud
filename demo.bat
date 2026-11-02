@echo off
title SISTEM INFORMASI MEDIS RUMAH SAKIT - KELOMPOK 4
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0demo.ps1"
pause

