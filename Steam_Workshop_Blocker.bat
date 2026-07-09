@echo off
title Steam Download Manager
color 0C

:: Find Steam Path from Registry
for /f "tokens=2*" %%A in ('reg query "HKCU\Software\Valve\Steam" /v SteamPath 2^>nul') do set "STEAM_PATH=%%B"

if "%STEAM_PATH%"=="" (
    echo [ERROR] Steam path not found in registry!
    set /p STEAM_PATH="Enter Steam Path manually (e.g. C:\Program Files (x86)\Steam): "
)

:: Replace forward slashes with backslashes
set "STEAM_PATH=%STEAM_PATH:/=\%"

:: Targets
set "WS_DOWNLOADS_PATH=%STEAM_PATH%\steamapps\workshop\downloads"
set "GAME_DOWNLOADS_PATH=%STEAM_PATH%\steamapps\downloading"

:MENU
cls
echo ===================================================
echo             STEAM DOWNLOAD MANAGER
echo ===================================================
echo Base Path: %STEAM_PATH%
echo ===================================================
echo.
echo --- WORKSHOP ---
echo 1. BLOCK Workshop Downloads
echo 2. UNBLOCK Workshop Downloads
echo.
echo --- ALL GAMES ---
echo 3. BLOCK All Game Downloads and Updates
echo 4. UNBLOCK All Game Downloads and Updates
echo.
echo --- SETTINGS ---
echo 5. Enter Custom Steam Library Path (if games on another drive)
echo 6. Exit
echo.
set /p CHOICE="Choose an option (1-6): "

if "%CHOICE%"=="1" goto BLOCK_WS
if "%CHOICE%"=="2" goto UNBLOCK_WS
if "%CHOICE%"=="3" goto BLOCK_ALL
if "%CHOICE%"=="4" goto UNBLOCK_ALL
if "%CHOICE%"=="5" goto CUSTOM
if "%CHOICE%"=="6" goto EOF
goto MENU

:BLOCK_WS
echo.
if not exist "%STEAM_PATH%\steamapps\workshop" mkdir "%STEAM_PATH%\steamapps\workshop" 2>nul
if not exist "%WS_DOWNLOADS_PATH%" mkdir "%WS_DOWNLOADS_PATH%" 2>nul
icacls "%WS_DOWNLOADS_PATH%" /deny Everyone:(W,WD,AD) /C /Q
echo [SUCCESS] Workshop downloads are now BLOCKED.
pause
goto MENU

:UNBLOCK_WS
echo.
if not exist "%WS_DOWNLOADS_PATH%" mkdir "%WS_DOWNLOADS_PATH%" 2>nul
icacls "%WS_DOWNLOADS_PATH%" /remove:d Everyone /C /Q
echo [SUCCESS] Workshop downloads are now UNBLOCKED.
pause
goto MENU

:BLOCK_ALL
echo.
if not exist "%STEAM_PATH%\steamapps" mkdir "%STEAM_PATH%\steamapps" 2>nul
if not exist "%GAME_DOWNLOADS_PATH%" mkdir "%GAME_DOWNLOADS_PATH%" 2>nul
icacls "%GAME_DOWNLOADS_PATH%" /deny Everyone:(W,WD,AD) /C /Q
echo [SUCCESS] ALL GAME downloads and updates are now BLOCKED.
pause
goto MENU

:UNBLOCK_ALL
echo.
if not exist "%GAME_DOWNLOADS_PATH%" mkdir "%GAME_DOWNLOADS_PATH%" 2>nul
icacls "%GAME_DOWNLOADS_PATH%" /remove:d Everyone /C /Q
echo [SUCCESS] ALL GAME downloads and updates are now UNBLOCKED.
pause
goto MENU

:CUSTOM
echo.
set /p STEAM_PATH="Enter Custom Path (e.g. D:\SteamLibrary): "
set "STEAM_PATH=%STEAM_PATH:/=\%"
set "WS_DOWNLOADS_PATH=%STEAM_PATH%\steamapps\workshop\downloads"
set "GAME_DOWNLOADS_PATH=%STEAM_PATH%\steamapps\downloading"
goto MENU

:EOF
exit
