@echo off
setlocal
cd /d %~dp0\..
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Release rmdir /s /q Release
python -m PyInstaller --noconfirm --clean --workpath build_temp --distpath dist_temp --specpath . --onedir --windowed --name "DataCanvas" --add-data "data;data" src/main.py
if errorlevel 1 exit /b 1
ren dist_temp dist
ren build_temp build
if exist Release rmdir /s /q Release
mkdir Release
xcopy /e /i /y dist\DataCanvas Release\DataCanvas >nul
if errorlevel 1 exit /b 1
echo Build complete: Release\DataCanvas\DataCanvas.exe
