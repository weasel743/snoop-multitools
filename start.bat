@echo off
title SNOOP - Multi-Tools
color 5F
cls

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║                                                               ║
echo  ║     ███████  ████  ██████  ███████    ████  ██████           ║
echo  ║     ██  ████ ██  ██ ██  ██ ██        ██  ██ ██               ║
echo  ║     ███████  ████  ██████  ███████    ████  ██████            ║
echo  ║                                                               ║
echo  ║              SNOOP - MULTI-TOOLS v1.0.0                      ║
echo  ║           Advanced Security Research Toolkit                  ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

echo  [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python is not installed or not in PATH.
    echo.
    echo  Please install Python 3.8 or higher from python.org
    echo  and make sure to check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

echo  [✔] Python found.
echo.

echo  [*] Launching SNOOP...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo  [!] SNOOP exited with an error.
    echo.
    pause
)