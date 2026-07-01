@echo off
title SNOOP - Installation Complete
color 0A

echo ============================================================
echo    ███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗
echo    ██╔════╝████╗  ██║██╔═══██╗██╔══██╗██╔══██╗
echo    ███████╗██╔██╗ ██║██║   ██║██████╔╝██████╔╝
echo    ╚════██║██║╚██╗██║██║   ██║██╔═══╝ ██╔══██╗
echo    ███████║██║ ╚████║╚██████╔╝██║     ██║  ██║
echo    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝
echo ============================================================
echo.
echo [*] Installation de TOUTES les dependances SNOOP
echo [*] Patience, cela peut prendre plusieurs minutes...
echo.

echo [1] Mise a jour de pip...
python -m pip install --upgrade pip -q
echo [✓] Pip mis a jour
echo.

echo [2] Installation des modules...
pip install colorama -q
pip install pystyle -q
pip install requests -q
pip install psutil -q
pip install pycryptodome -q
pip install pypiwin32 -q
pip install comtypes -q
pip install Pillow -q
pip install opencv-python -q
pip install selenium -q
pip install webdriver-manager -q
pip install discord.py -q
pip install aiohttp -q
pip install dnspython -q
pip install beautifulsoup4 -q
pip install pysocks -q
pip install websocket-client -q
pip install piexif -q
pip install exifread -q
pip install mutagen -q
pip install python-whois -q
pip install phonenumbers -q
pip install pynput -q
pip install pywin32 -q
pip install mnemonic -q
pip install stem -q
pip install pyautogui -q
pip install mss -q
pip install pyperclip -q
pip install flask -q
pip install werkzeug -q
pip install numpy -q
pip install pyinstaller -q
echo [✓] Modules installes
echo.

echo [3] Creation des dossiers...
mkdir core 2>nul
mkdir input 2>nul
mkdir output 2>nul
mkdir build_output 2>nul
mkdir dist 2>nul
mkdir stub 2>nul
echo [✓] Dossiers crees
echo.

echo [4] Fichier config...
echo {} > core\config.json
echo. > core\__init__.py
echo [✓] Config creee
echo.

echo ============================================================
echo [✓] INSTALLATION TERMINEE !
echo.
echo    Pour lancer SNOOP :
echo    python main.py
echo.
echo ============================================================
pause
