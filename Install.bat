@echo off
setlocal
title YouTubeLiteClient Lite - Installer

:: ============================
:: MOVE TO SCRIPT DIR
:: ============================
cd /d "%~dp0"

:: ============================
:: CHECK ADMIN
:: ============================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: ============================
:: VARIABLES
:: ============================
set APP_NAME=YouTubeLiteClient Lite
set INSTALL_DIR=%ProgramFiles%\YouTubeLiteClientLite
set DESKTOP=%Public%\Desktop

echo Installing %APP_NAME%...
echo.

:: ============================
:: CREATE INSTALL DIR
:: ============================
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: ============================
:: COPY FILES
:: ============================
copy /Y "main32.exe" "%INSTALL_DIR%" >nul
copy /Y "yt-dlp.exe" "%INSTALL_DIR%" >nul
copy /Y "README.txt" "%INSTALL_DIR%" >nul

:: ============================
:: CREATE DESKTOP SHORTCUT
:: ============================
powershell -Command ^
 "$s=(New-Object -COM WScript.Shell).CreateShortcut('%DESKTOP%\YouTubeLiteClient Lite.lnk');" ^
 "$s.TargetPath='%INSTALL_DIR%\main32.exe';" ^
 "$s.WorkingDirectory='%INSTALL_DIR%';" ^
 "$s.IconLocation='%INSTALL_DIR%\main32.exe';" ^
 "$s.Save()"

:: ============================
:: DONE
:: ============================
echo.
echo Installation completed successfully.
echo Installed in:
echo %INSTALL_DIR%
echo.
pause
