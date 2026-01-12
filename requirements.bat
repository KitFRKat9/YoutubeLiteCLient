@echo off
setlocal EnableDelayedExpansion
title YouTubeLiteClient - Dependency Check
cd /d "%~dp0"

echo ===============================
echo   YouTubeLiteClient - Check
echo ===============================
echo.

REM === CHECK VLC ===
set "VLC_PATH="

if exist "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" (
    set "VLC_PATH=C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    echo [OK] VLC found - 32 bit
)

if not defined VLC_PATH if exist "C:\Program Files\VideoLAN\VLC\vlc.exe" (
    set "VLC_PATH=C:\Program Files\VideoLAN\VLC\vlc.exe"
    echo [OK] VLC found - 64 bit
)

if not defined VLC_PATH (
    echo [ERROR] VLC not found
    echo Opening VLC download page...
    start https://www.videolan.org/vlc/
    echo.
    echo Install VLC, then restart this script.
    pause
    exit /b
)

REM === CHECK yt-dlp ===
if exist "yt-dlp.exe" (
    echo [OK] yt-dlp found
) else (
    echo [INFO] yt-dlp not found, downloading...
    powershell -Command ^
     "Invoke-WebRequest https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe -OutFile yt-dlp.exe"

    if exist "yt-dlp.exe" (
        echo [OK] yt-dlp downloaded
    ) else (
        echo [ERROR] Failed to download yt-dlp
        pause
        exit /b
    )
)

cls
echo VLC Installed.
echo yt.dlp.exe Downloaded.
echo.
echo You are good to go, to open the client open YoutubeLiteClient.exe
pause
