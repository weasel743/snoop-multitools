@echo off
title SNOOP Toolkit - Installation des dependances
echo ============================================================
echo       Installation des dependances pour SNOOP Toolkit
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8 ou superieur depuis https://python.org
    pause
    exit /b 1
)

echo [OK] Python detecte.
echo.

echo Mise a jour de pip...
python -m pip install --upgrade pip
echo.

echo Installation des paquets requis...
echo.

pip install pystyle
pip install requests
pip install selenium
pip install dnspython
pip install beautifulsoup4
pip install pysocks
pip install websocket-client
pip install piexif
pip install exifread
pip install mutagen
pip install PyQt5
pip install colorama
pip install webdriver-manager
pip install pillow
pip install flask
pip install werkzeug
pip install aiohttp
pip install psutil
pip install whois
pip install phonenumbers
pip install pynput
pip install pywin32
pip install mnemonic
pip install stem
pip install pycryptodome
pip install discord.py
pip install opencv-python
pip install numpy
pip install pyautogui
pip install mss
pip install pyperclip
pip install browserhistory
pip install pyinstaller

echo.
echo Tentative d'installation de pyaudio (optionnel - peut echouer)...

pip install pyaudio
if errorlevel 1 (
    echo [AVERTISSEMENT] Echec de l'installation de pyaudio.
    echo Vous pouvez l'installer plus tard via :
    echo   pip install pipwin
    echo   pipwin install pyaudio
)

echo.
echo ============================================================
echo Installation terminee !
echo Il est recommande d'installer UPX pour compresser les EXE.
echo Telechargez UPX depuis https://upx.github.io/ et placez upx.exe dans le PATH.
echo ============================================================
pause