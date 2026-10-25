@echo off
cd /d "%~dp0"
echo Starting Node Server...
start cmd /k "node server.js"
timeout /t 5 /nobreak >nul
echo Starting Python Ear...
start cmd /k "python jarvis_ear.py"
echo.
echo If you see errors in the new windows, take a screenshot!
pause