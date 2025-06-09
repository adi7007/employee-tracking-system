@echo off
echo Killing running instances of main.exe...
taskkill /f /im main.exe >nul 2>&1

echo.
echo Cleaning previous builds...
rmdir /s /q build
rmdir /s /q dist
del /q main.spec

echo.
echo Rebuilding executable using PyInstaller...
pyinstaller --onefile --windowed main.py

echo.
echo Done! Your new executable is in the "dist" folder.
pause
