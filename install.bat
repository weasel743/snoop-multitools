@echo off
title SNOOP - Installation des dépendances
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
echo [*] Installation des dépendances pour SNOOP GRABBER v3.0
echo [*] Ce script va installer tous les modules nécessaires
echo.
echo ============================================================
echo.

REM ============================================================
REM Vérification de Python
REM ============================================================
echo [1] Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python n'est pas installé !
    echo [X] Veuillez installer Python depuis https://python.org
    echo [X] N'oubliez pas de cocher "Add Python to PATH"
    pause
    exit /b 1
)
echo [✓] Python trouvé !
echo.

REM ============================================================
REM Mise à jour de pip
REM ============================================================
echo [2] Mise à jour de pip...
python -m pip install --upgrade pip >nul 2>&1
echo [✓] Pip mis à jour !
echo.

REM ============================================================
REM Installation des modules principaux
REM ============================================================
echo [3] Installation des modules principaux...
echo.

echo     [+] Installation de colorama...
pip install colorama >nul 2>&1

echo     [+] Installation de pystyle...
pip install pystyle >nul 2>&1

echo     [+] Installation de requests...
pip install requests >nul 2>&1

echo     [+] Installation de psutil...
pip install psutil >nul 2>&1

echo     [+] Installation de pycryptodome...
pip install pycryptodome >nul 2>&1

echo     [+] Installation de pypiwin32 (win32crypt)...
pip install pypiwin32 >nul 2>&1

echo     [+] Installation de comtypes...
pip install comtypes >nul 2>&1

echo     [+] Installation de Pillow (PIL)...
pip install Pillow >nul 2>&1

echo     [+] Installation de opencv-python (cv2)...
pip install opencv-python >nul 2>&1

echo     [+] Installation de selenium...
pip install selenium >nul 2>&1

echo     [+] Installation de webdriver-manager...
pip install webdriver-manager >nul 2>&1

echo     [+] Installation de tkinter (intégré à Python)...
echo     [✓] tkinter est inclus avec Python

echo     [+] Installation de pyinstaller...
pip install pyinstaller >nul 2>&1

echo     [+] Installation de numpy...
pip install numpy >nul 2>&1

echo.
echo [✓] Modules principaux installés !
echo.

REM ============================================================
REM Vérification des installations
REM ============================================================
echo [4] Vérification des installations...
echo.

set MISSING=0

python -c "import colorama" >nul 2>&1
if errorlevel 1 ( echo [X] colorama manquant & set MISSING=1 ) else ( echo [✓] colorama OK )

python -c "import pystyle" >nul 2>&1
if errorlevel 1 ( echo [X] pystyle manquant & set MISSING=1 ) else ( echo [✓] pystyle OK )

python -c "import requests" >nul 2>&1
if errorlevel 1 ( echo [X] requests manquant & set MISSING=1 ) else ( echo [✓] requests OK )

python -c "import psutil" >nul 2>&1
if errorlevel 1 ( echo [X] psutil manquant & set MISSING=1 ) else ( echo [✓] psutil OK )

python -c "from Crypto.Cipher import AES" >nul 2>&1
if errorlevel 1 ( echo [X] pycryptodome manquant & set MISSING=1 ) else ( echo [✓] pycryptodome OK )

python -c "import win32crypt" >nul 2>&1
if errorlevel 1 ( echo [X] pypiwin32 manquant & set MISSING=1 ) else ( echo [✓] pypiwin32 OK )

python -c "import comtypes" >nul 2>&1
if errorlevel 1 ( echo [X] comtypes manquant & set MISSING=1 ) else ( echo [✓] comtypes OK )

python -c "from PIL import ImageGrab" >nul 2>&1
if errorlevel 1 ( echo [X] Pillow manquant & set MISSING=1 ) else ( echo [✓] Pillow OK )

python -c "import cv2" >nul 2>&1
if errorlevel 1 ( echo [X] opencv-python manquant & set MISSING=1 ) else ( echo [✓] opencv-python OK )

python -c "import selenium" >nul 2>&1
if errorlevel 1 ( echo [X] selenium manquant & set MISSING=1 ) else ( echo [✓] selenium OK )

python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 ( echo [X] pyinstaller manquant & set MISSING=1 ) else ( echo [✓] pyinstaller OK )

echo.

if %MISSING%==1 (
    echo [⚠] Certains modules sont manquants. Réessayez l'installation.
    echo [⚠] Ou installez-les manuellement avec : pip install [nom_module]
) else (
    echo [✓] TOUS les modules sont installés correctement !
)

echo.
echo ============================================================
echo [✓] Installation terminée !
echo.
echo    Pour lancer le panel :
echo    python panel_complete.py
echo.
echo    Pour lancer le menu :
echo    python main.py
echo.
echo    Pour générer un grabber :
echo    python main.py puis option 1
echo.
echo ============================================================
pause
