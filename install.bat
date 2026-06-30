@echo off
title SNOOP Multi-Tools - Installer
color 0A

echo.
echo   ╔═══════════════════════════════════════╗
echo   ║     SNOOP Multi-Tools Installer      ║
echo   ╚═══════════════════════════════════════╝
echo.

echo [*] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python non trouve. Installez Python 3.8+
    pause
    exit
)
python --version
echo.

echo [*] Installation des dependances...
pip install --upgrade pip -q
pip install pystyle colorama psutil requests aiohttp selenium webdriver-manager beautifulsoup4 dnspython whois phonenumbers pynput pywin32 pillow cryptography mnemonic pycryptodome flask werkzeug pysocks websocket-client -q

echo.
echo [*] Verification des dossiers...
if not exist "core" mkdir core
if not exist "stub" mkdir stub
if not exist "output" mkdir output
if not exist "input" mkdir input

echo.
echo [*] Creation des fichiers d'input...
if not exist "input\proxies.txt" echo # Proxies > input\proxies.txt
if not exist "input\roblox_usernames.txt" echo # Roblox Usernames > input\roblox_usernames.txt

echo.
echo   ╔═══════════════════════════════════════╗
echo   ║    Installation terminee !           ║
echo   ║    Lancez main.py pour demarrer      ║
echo   ╚═══════════════════════════════════════╝
echo.

pause