# ================================================================================================
# SNOOP PAGINATED UI – MATRIX EDITION AVEC THÈMES
# Banner SNOOP original, changement de thème fonctionnel, style matrix
# Navigation : 1-7 / B / N / H / Q
# Stats : CPU + RAM (sans IP)
# ================================================================================================

import os
import sys
import shutil
import re
import time
import random
import socket
from typing import List, Tuple, Dict, Optional

try:
    import psutil
except ImportError:
    psutil = None

from pystyle import Center
from core.display import Theme, Colorate, Colors, clr, get_config

if os.name == "nt":
    import msvcrt
else:
    import tty
    import termios

# ================================================================================================
# CONSTANTES & UTILITAIRES
# ================================================================================================

ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(t):
    return ANSI_RE.sub('', t)

def term_w():
    return shutil.get_terminal_size().columns

def box_w():
    tw = term_w()
    return max(80, min(120, tw - 4))

def margin(bw):
    tw = term_w()
    return " " * max(0, (tw - bw) // 2)

def trunc(t, ml, sfx="..."):
    if len(t) <= ml:
        return t
    return t[:ml - len(sfx)] + sfx

def get_stats():
    cpu, ram = 0, 0
    if psutil:
        try:
            cpu = int(psutil.cpu_percent(interval=0.05))
            ram = int(psutil.virtual_memory().percent)
        except:
            pass
    return cpu, ram

# ================================================================================================
# BANNER SNOOP ORIGINAL
# ================================================================================================

BANNER = r"""
  .-')        .-') _                       _ (`-.        .-') _                                         .-')    
 ( OO ).     ( OO ) )                     ( (OO  )      (  OO) )                                       ( OO ).  
(_)---\_),--./ ,--,'   .----.    .----.  _.`     \      /     '._  .-'),-----.  .-'),-----.  ,--.     (_)---\_) 
/    _ | |   \ |  |\  /  ..  \  /  ..  \(__...--''      |'--...__)( OO'  .-.  '( OO'  .-.  ' |  |.-') /    _ |  
\  :` `. |    \|  | ).  /  \  ..  /  \  .|  /  | |      '--.  .--'/   |  | |  |/   |  | |  | |  | OO )\  :` `.  
 '..`''.)|  .     |/ |  |  '  ||  |  '  ||  |_.' |         |  |   \_) |  |\|  |\_) |  |\|  | |  |`-' | '..`''.) 
.-._)   \|  |\    |  '  \  /  ''  \  /  '|  .___.'         |  |     \ |  | |  |  \ |  | |  |(|  '---.'.-._)   \ 
\       /|  | \   |   \  `'  /  \  `'  / |  |              |  |      `'  '-'  '   `'  '-'  ' |      | \       / 
 `-----' `--'  `--'    `---''    `---''  `--'              `--'        `-----'      `-----'  `------'  `-----'
"""

# ================================================================================================
# PAGES – TOUTES LES CATÉGORIES
# ================================================================================================

PAGES = [
    {
        "title": "MALICIOUS",
        "description": "Payloads, DDoS, scanners",
        "tools": [
            ("01", "Make Grabber", "Compile password & token stealers"),
            ("02", "Make RAT", "Build Remote Access Trojans"),
            ("03", "Make IP Grabber", "Generate IP tracking links"),
            ("04", "Make Keylogger", "Build stealth keyloggers"),
            ("05", "Crypto Scanner", "Scan for crypto wallets"),
            ("06", "Mail Bomber", "Send spam emails"),
            ("07", "DDoS Attack", "Network stress tests"),
            ("08", "Vuln Scanner", "Scan for vulnerabilities"),
            ("09", "Blocker", "Remote keyboard/mouse blocker"),
        ]
    },
    {
        "title": "DISCORD",
        "description": "Tokens, raid, webhooks",
        "tools": [
            ("01", "Selfbot", "Custom Discord selfbot"),
            ("02", "Raid / Nuke", "Destroy Discord servers"),
            ("03", "Webhook Spam", "Spam Discord webhooks"),
            ("04", "Webhook Delete", "Delete Discord webhooks"),
            ("05", "Token Info", "Get token information"),
            ("06", "Token Login", "Automated token login"),
            ("07", "Token Nuker", "Destroy Discord accounts"),
            ("08", "Token Rotator", "Rotate statuses"),
            ("09", "Token Onliner", "Keep tokens online"),
            ("10", "ID to Token", "Bruteforce tokens"),
            ("11", "Server Cloner", "Clone Discord servers"),
            ("12", "Server Info", "Get guild information"),
            ("13", "Username Checker", "Check username availability"),
            ("14", "Report Bot", "Automated reporting"),
            ("15", "Bot Invite", "Generate bot invites"),
        ]
    },
    {
        "title": "OSINT",
        "description": "IP, DNS, phone, dox",
        "tools": [
            ("01", "IP Lookup", "Geolocate IP addresses"),
            ("02", "Email Lookup", "OSINT on emails"),
            ("03", "Phone Lookup", "Phone number intelligence"),
            ("04", "Username Tracker", "Track across platforms"),
            ("05", "Whois Lookup", "Domain registration details"),
            ("06", "DNS Enumeration", "DNS records lookup"),
            ("07", "Subdomain Finder", "Find subdomains"),
            ("08", "Port Scanner", "Advanced port scanning"),
            ("09", "Shodan Search", "Shodan database search"),
            ("10", "Wayback Machine", "View website archives"),
            ("11", "Social Scraper", "Social media presence"),
            ("12", "Email Verifier", "Verify email addresses"),
            ("13", "Pastebin Dorking", "Search Pastebin"),
            ("14", "GeoIP Location", "Geographic location"),
            ("15", "Dox Creator", "Create dox profiles"),
        ]
    },
    {
        "title": "TOOLS",
        "description": "Binder, crypter, obfuscator",
        "tools": [
            ("01", "Binder", "Bind executables"),
            ("02", "Crypter", "Encrypt executables"),
            ("03", "Fusion", "Merge Grabber & RAT"),
            ("04", "Crypted RAT", "FUD RAT builder"),
            ("05", "Crypted Grabber", "FUD grabber builder"),
            ("06", "USB Worm", "Create USB worm"),
            ("07", "Network Scanner", "Scan local network"),
            ("08", "Phishing Page", "Generate phishing pages"),
            ("09", "Proxy Scraper", "Scrape proxies"),
            ("10", "Proxy Checker", "Test proxies"),
            ("11", "Website Cloner", "Clone websites"),
            ("12", "Python Obfuscator", "Obfuscate Python code"),
        ]
    },
    {
        "title": "LOGIN",
        "description": "Token & cookie login",
        "tools": [
            ("01", "Token Login", "Login with Discord token"),
            ("02", "Cookie Login", "Login with cookies"),
        ]
    },
    {
        "title": "ROBLOX",
        "description": "User, cookie, group",
        "tools": [
            ("01", "User Info", "Get Roblox user info"),
            ("02", "Cookie Info", "Extract cookie data"),
            ("03", "Cookie Login", "Automated cookie login"),
            ("04", "Cookie Refresher", "Refresh cookies"),
            ("05", "Group Info", "Get group information"),
            ("06", "Asset Download", "Download assets"),
            ("07", "Name History", "Username history"),
            ("08", "Username Checker", "Check availability"),
            ("09", "Generate Usernames", "Generate usernames"),
        ]
    },
    {
        "title": "SETTINGS",
        "description": "Configuration",
        "tools": [
            ("01", "Clear Settings", "Reset all settings"),
        ]
    }
]

CAT_SHORT = ["MALIC", "DISC", "OSINT", "TOOLS", "LOGIN", "RBLX", "SET"]

# ================================================================================================
# FONCTIONS D'AFFICHAGE – MATRIX AVEC THÈMES
# ================================================================================================

def get_theme_colors():
    return Theme.get_colors()

def draw_matrix_header(active_idx, bw):
    inner = bw - 2
    m = margin(bw)
    colors = get_theme_colors()
    reset = Colors.reset
    
    # Ligne supérieure
    print(m + Colorate.Horizontal(colors["sub"], "┌" + "─" * inner + "┐"))
    
    # Catégories
    tabs = []
    for i, name in enumerate(CAT_SHORT):
        if i == active_idx:
            tabs.append(Colorate.Horizontal(colors["head"], f"▶{name}◀"))
        else:
            tabs.append(Colorate.Horizontal(colors["num"], name))
    
    tab_line = "  ".join(tabs)
    plain_len = len(strip_ansi(tab_line))
    pad = max(0, (inner - plain_len) // 2)
    extra = max(0, inner - plain_len - pad * 2)
    
    print(m + Colorate.Horizontal(colors["sub"], "│") + " " * pad + tab_line + " " * pad + " " * extra + Colorate.Horizontal(colors["sub"], "│"))
    
    # Ligne inférieure
    print(m + Colorate.Horizontal(colors["sub"], "├" + "─" * inner + "┤"))

def draw_matrix_tools(active_idx, bw):
    page = PAGES[active_idx]
    inner = bw - 2
    m = margin(bw)
    colors = get_theme_colors()
    
    # Titre de la catégorie
    title = f" {page['title']} — {page['description']} "
    if len(strip_ansi(title)) > inner:
        title = f" {page['title']} "
    bl = max(2, (inner - len(strip_ansi(title))) // 2)
    ex = "─" if (inner - len(strip_ansi(title))) % 2 else ""
    
    top = Colorate.Horizontal(colors["num"], "┌") + Colorate.Horizontal(colors["sub"], "─" * bl) + Colorate.Horizontal(colors["head"], title) + Colorate.Horizontal(colors["sub"], "─" * bl + ex) + Colorate.Horizontal(colors["num"], "┐")
    print(m + top)
    print(m + Colorate.Horizontal(colors["sub"], "├" + "─" * inner + "┤"))
    
    # Liste des outils
    for num, name, desc in page["tools"]:
        num_part = Colorate.Horizontal(colors["num"], f"[{num}]")
        name_part = Colorate.Horizontal(colors["txt"], f"{name:<20}")
        desc_part = Colorate.Horizontal(colors["sub"], desc)
        line = num_part + "  " + name_part + "  " + desc_part
        
        if len(strip_ansi(line)) > inner:
            line = line[:inner-3] + "..."
        pad = max(0, inner - len(strip_ansi(line)))
        print(m + Colorate.Horizontal(colors["sub"], "│") + line + " " * pad + Colorate.Horizontal(colors["sub"], "│"))
    
    print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

def draw_matrix_footer(bw):
    inner = bw - 2
    m = margin(bw)
    cpu, ram = get_stats()
    colors = get_theme_colors()
    
    # Barres de progression
    cpu_bar = "█" * min(cpu // 5, 20)
    ram_bar = "█" * min(ram // 5, 20)
    
    cpu_text = Colorate.Horizontal(colors["num"], f"CPU {cpu:>2}%") + Colorate.Horizontal(colors["sub"], f" [{cpu_bar:<20}]")
    ram_text = Colorate.Horizontal(colors["num"], f"RAM {ram:>2}%") + Colorate.Horizontal(colors["sub"], f" [{ram_bar:<20}]")
    
    info = f"{cpu_text}  {ram_text}"
    plain_info = strip_ansi(info)
    pad_info = max(0, (inner - len(plain_info)) // 2)
    extra_info = max(0, inner - len(plain_info) - pad_info * 2)
    line = " " * pad_info + info + " " * pad_info + " " * extra_info
    
    # Navigation
    nav = (Colorate.Horizontal(colors["sub"], "[") + Colorate.Horizontal(colors["num"], "1-7") + Colorate.Horizontal(colors["sub"], "]") + " Cat  " +
           Colorate.Horizontal(colors["sub"], "[") + Colorate.Horizontal(colors["num"], "B") + Colorate.Horizontal(colors["sub"], "]") + " Back  " +
           Colorate.Horizontal(colors["sub"], "[") + Colorate.Horizontal(colors["num"], "N") + Colorate.Horizontal(colors["sub"], "]") + " Next  " +
           Colorate.Horizontal(colors["sub"], "[") + Colorate.Horizontal(colors["num"], "H") + Colorate.Horizontal(colors["sub"], "]") + " Help  " +
           Colorate.Horizontal(colors["sub"], "[") + Colorate.Horizontal(colors["head"], "Q") + Colorate.Horizontal(colors["sub"], "]") + " Quit")
    
    plain_nav = strip_ansi(nav)
    nav_pad = max(0, (inner - len(plain_nav)) // 2)
    nav_extra = max(0, inner - len(plain_nav) - nav_pad * 2)
    nav_line = " " * nav_pad + nav + " " * nav_pad + " " * nav_extra
    
    print(m + Colorate.Horizontal(colors["sub"], "├" + "─" * inner + "┤"))
    print(m + Colorate.Horizontal(colors["sub"], "│") + line + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "│") + nav_line + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

# ================================================================================================
# DASHBOARD PRINCIPAL
# ================================================================================================

def dashboard(idx):
    clr()
    bw = box_w()
    colors = get_theme_colors()
    
    hostname = socket.gethostname()
    ver = get_config().get("version", "1.0.0")
    
    # Header
    header = Colorate.Horizontal(colors["head"], f"SNOOP v{ver}") + Colorate.Horizontal(colors["sub"], "  │  ") + Colorate.Horizontal(colors["num"], f"@{hostname}")
    print(Center.XCenter(header))
    print()
    
    # Banner
    lines = BANNER.strip('\n').splitlines()
    for line in lines:
        if line.strip():
            print(Colorate.Horizontal(colors["banner"], Center.XCenter(line)))
    print()
    
    draw_matrix_header(idx, bw)
    print()
    draw_matrix_tools(idx, bw)
    print()
    draw_matrix_footer(bw)

# ================================================================================================
# GESTION DES TOUCHES
# ================================================================================================

def getch_timeout(timeout_sec):
    if os.name == "nt":
        start = time.time()
        while time.time() - start < timeout_sec:
            if msvcrt.kbhit():
                return msvcrt.getch().decode("utf-8", errors="ignore").lower()
            time.sleep(0.05)
        return None
    else:
        import select
        rlist, _, _ = select.select([sys.stdin], [], [], timeout_sec)
        if rlist:
            return sys.stdin.read(1).lower()
        return None

def run():
    idx = 0
    dashboard(idx)
    while True:
        key = getch_timeout(1.0)
        if key is None:
            continue

        if key in ("q", "\x1b"):
            clr()
            colors = get_theme_colors()
            print(Colorate.Horizontal(colors["head"], "SNOOP terminated."))
            break
        elif key in ("\r", "\n", " "):
            print()
            colors = get_theme_colors()
            page = PAGES[idx]
            print(Colorate.Horizontal(colors["num"], f"  -> {page['title']} selected"))
            time.sleep(0.2)
            input(Colorate.Horizontal(colors["num"], "  Press Enter to return..."))
            dashboard(idx)
        elif key == "h":
            clr()
            colors = get_theme_colors()
            m = " " * max(0, (term_w() - 60) // 2)
            
            print(m + Colorate.Horizontal(colors["head"], "  H E L P"))
            print()
            print(m + Colorate.Horizontal(colors["num"], "  1-7") + "  : Change category")
            print(m + Colorate.Horizontal(colors["num"], "  B") + "       : Previous category")
            print(m + Colorate.Horizontal(colors["num"], "  N") + "       : Next category")
            print(m + Colorate.Horizontal(colors["num"], "  Enter") + "   : Select current category")
            print(m + Colorate.Horizontal(colors["num"], "  H") + "       : Show this help")
            print(m + Colorate.Horizontal(colors["head"], "  Q") + "       : Quit")
            print()
            print(m + Colorate.Horizontal(colors["sub"], "Categories:"))
            for i, cat in enumerate(CAT_SHORT, 1):
                print(m + f"  {Colorate.Horizontal(colors['num'], str(i))} - {cat}")
            print()
            input(Colorate.Horizontal(colors["num"], "  Press Enter to continue..."))
            dashboard(idx)
        elif key in ("b", ","):
            idx = (idx - 1) % len(PAGES)
            dashboard(idx)
        elif key in ("n", "."):
            idx = (idx + 1) % len(PAGES)
            dashboard(idx)
        elif key in ("1", "2", "3", "4", "5", "6", "7"):
            idx = int(key) - 1
            dashboard(idx)

# ================================================================================================
# CLASSE PaginatedUI – COMPATIBLE AVEC main.py
# ================================================================================================

class PaginatedUI:
    @staticmethod
    def get_layout_width():
        return box_w()

    @staticmethod
    def get_margin(bw):
        return margin(bw)

    @classmethod
    def draw_radar(cls, active_idx, colors, bw, m):
        pass

    @classmethod
    def draw_tools_list(cls, active_idx, colors, bw, m):
        draw_matrix_tools(active_idx, bw)

    @classmethod
    def draw_header(cls, colors, bw, m):
        pass

    @classmethod
    def draw_footer(cls, colors, bw, m):
        draw_matrix_footer(bw)

    @classmethod
    def draw_dashboard(cls, active_idx):
        dashboard(active_idx)

    @staticmethod
    def draw_card_box(title, items, theme_colors=None):
        colors = theme_colors or Theme.get_colors()
        tw = term_w()
        bw = max(50, min(80, tw - 6))
        inner = bw - 2
        m = " " * max(0, (tw - bw) // 2)
        bl = max(2, (inner - len(title)) // 2)
        ex = "─" if (inner - len(title)) % 2 else ""
        top = "┌" + "─" * bl + title + "─" * bl + ex + "┐"
        if len(strip_ansi(top)) > bw:
            top = top[:bw - 1] + "┐"
        print()
        print(m + Colorate.Horizontal(colors["sub"], top))
        print(m + Colorate.Horizontal(colors["sub"], "│") + " " * inner + Colorate.Horizontal(colors["sub"], "│"))
        cw = (inner - 2) // 2
        il = list(items.items())
        for i in range(0, len(il), 2):
            k1, v1 = il[i]
            k2, v2 = il[i + 1] if i + 1 < len(il) else ("", "")
            mv1 = max(0, cw - len(k1) - 5)
            mv2 = max(0, cw - len(k2) - 5)
            va1 = trunc(v1, mv1)
            va2 = trunc(v2, mv2) if k2 else ""
            c1 = f"  [{k1}] {va1:<{mv1}}"
            c2 = f"  [{k2}] {va2:<{mv2}}" if k2 else " " * cw
            plain = c1 + c2
            pad = max(0, inner - len(strip_ansi(plain)))
            row = (Colorate.Horizontal(colors["num"], "│") + " " +
                   Colorate.Horizontal(colors["num"], f"  [{k1}]") + " " +
                   Colorate.Horizontal(colors["txt"], f"{va1:<{mv1}}") +
                   (Colorate.Horizontal(colors["num"], f"  [{k2}]") + " " + Colorate.Horizontal(colors["txt"], f"{va2:<{mv2}}")
                    if k2 else " " * cw) + " " * pad + Colorate.Horizontal(colors["num"], "│"))
            print(m + row)
        print(m + Colorate.Horizontal(colors["sub"], "│") + " " * inner + Colorate.Horizontal(colors["sub"], "│"))
        print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

# ================================================================================================
# MAIN
# ================================================================================================

if __name__ == "__main__":
    try:
        if term_w() < 60:
            colors = get_theme_colors()
            print(Colorate.Horizontal(colors["head"], "Error: Terminal too small."))
            sys.exit(1)
        run()
    except KeyboardInterrupt:
        clr()
        colors = get_theme_colors()
        print()