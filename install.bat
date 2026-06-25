@echo off
title Installation des dépendances - SNOOP
color 0A
echo ========================================
echo  INSTALLATION DES PAQUETS PYTHON
echo ========================================
echo.

:: Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouve. Installe Python 3.8+ depuis python.org
    pause
    exit /b 1
)

:: Mettre à jour pip
python -m pip install --upgrade pip -q

:: Installer les paquets (liste complète, sans doublons)
echo Installation en cours...
pip install -q flask pyinstaller pystyle colorama requests aiohttp beautifulsoup4 selenium webdriver-manager pillow opencv-python pynput pyperclip pywin32 psutil pyaudio wave numpy browserhistory cryptography mss discord.py mnemonic stem PySocks whois phonenumbers dnspython websocket-client piexif exifread mutagen PyQt5 werkzeug

echo.
echo [SUCCES] Toutes les dependances sont installees.
echo.
pause
