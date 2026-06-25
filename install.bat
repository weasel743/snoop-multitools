@echo off
title Installation des dépendances - SNOOP
color 0A
echo ============================================================
echo  INSTALLATION COMPLETE DES PAQUETS PYTHON POUR SNOOP
echo ============================================================
echo.

:: Vérifier la présence de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo          Telechargez Python 3.8 ou superieur depuis python.org
    pause
    exit /b 1
)

:: Mise à jour de pip, setuptools et wheel
echo [1/4] Mise a jour de pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel -q

:: Installation des paquets principaux (sans pyaudio et MySQL)
echo [2/4] Installation des paquets Python (peut prendre 2-3 minutes)...
pip install -q flask pyinstaller pystyle colorama requests aiohttp beautifulsoup4 selenium webdriver-manager pillow opencv-python pynput pyperclip pywin32 psutil numpy browserhistory cryptography mss discord.py mnemonic stem PySocks whois phonenumbers dnspython websocket-client piexif exifread mutagen PyQt5 werkzeug pycryptodome comtypes pyautogui

:: Installation de pipwin si absent
echo [3/4] Preparation de pipwin pour pyaudio...
pip show pipwin >nul 2>&1
if errorlevel 1 (
    pip install pipwin -q
)

:: Installation de pyaudio via pipwin (évite la compilation)
echo [4/4] Installation de pyaudio via pipwin...
pipwin install pyaudio -q

echo.
echo ============================================================
echo  [SUCCES] Toutes les dependances sont installees.
echo  [INFO]  Si une erreur persiste sur pyaudio, lancez manuellement :
echo         pipwin install pyaudio
echo ============================================================
pause
