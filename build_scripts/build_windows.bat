@echo off
REM Build script for Windows
REM This script creates a distributable version of Load Tester

echo ============================================
echo Building Load Tester for Windows
echo ============================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Check if ab.exe exists
if not exist "vendor\ab\windows\ab.exe" (
    echo.
    echo ERROR: ab.exe not found!
    echo Please place ab.exe in vendor\ab\windows\
    echo See vendor\ab\README.md for instructions.
    echo.
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Run PyInstaller
echo.
echo Running PyInstaller...
pyinstaller build.spec

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Build successful!
echo Output: dist\LoadTester\
echo ============================================
echo.
echo To run the application:
echo   dist\LoadTester\LoadTester.exe
echo.
pause
