@echo off
chcp 65001 > nul
echo.
echo ╔══════════════════════════════════════════╗
echo ║     أداة اختبار الحمل - Load Tester     ║
echo ╚══════════════════════════════════════════╝
echo.
cd /d "%~dp0"
python src/main.py
pause
