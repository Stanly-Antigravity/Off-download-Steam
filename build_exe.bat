@echo off
title Build Steam Manager GUI PRO
color 0B

echo ===================================================
echo     Installing Dependencies and Building EXE
echo ===================================================
echo.

echo Installing customtkinter, pyinstaller, and Pillow...
pip install customtkinter pyinstaller Pillow

echo.
echo Converting PNG to ICO...
python -c "from PIL import Image; Image.open('icon.png').save('icon.ico', format='ICO', sizes=[(256, 256)])"

echo.
echo Cleaning old files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q Steam_Manager_Pro.spec 2>nul

echo.
echo Building FAST-LOAD EXE (No OneFile)...
:: Removed --onefile for instant loading speed.
pyinstaller --noconsole --icon="icon.ico" --name "Steam_Manager_Pro" --add-data "icon.png;." --add-data "icon.ico;." gui_app.py

echo.
echo ===================================================
echo Build Complete! 
echo Go to the "dist\Steam_Manager_Pro" folder.
echo Run "Steam_Manager_Pro.exe" (Loads instantly!)
echo ===================================================
pause
