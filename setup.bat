@echo off
title Jarvis AI - Setup & Launch
color 0B

echo ===================================================
echo       WELCOME TO JARVIS AI - ONE CLICK SETUP
echo ===================================================
echo.

:: Check if Node.js is installed
node -v >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Node.js is not installed!
    echo Please download and install it from: https://nodejs.org/
    echo After installing, restart this setup file.
    pause
    exit
)

echo [1/3] Installing dependencies (This might take a minute)...
call npm install express cors groq-sdk multer
echo.

echo [2/3] Starting the Server...
echo (Do not close this window while using Jarvis)
start "Jarvis Server" cmd /c "node server.js"
echo.

echo [3/3] Opening Jarvis in your browser...
timeout /t 3 /nobreak >nul
start http://localhost:3000/avatar.html

echo.
echo ===================================================
echo SETUP COMPLETE! 
echo You can close this window now.
echo (The Jarvis Server is running in the background)
echo ===================================================
timeout /t 5 >nul
exit