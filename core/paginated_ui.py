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

ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(t):
    return ANSI_RE.sub('', t)

def term_w():
    return shutil.get_terminal_size().columns

def box_w():
    tw = term_w()
    return max(74, min(100, tw - 4))

def margin(bw):
    tw = term_w()
    return " " * max(0, (tw - bw) // 2)

def trunc(t, ml, sfx="..."):
    if len(t) <= ml:
        return t
    return t[:ml - len(sfx)] + sfx

def get_stats():
    if not psutil:
        return 0, 0
    try:
        cpu = int(psutil.cpu_percent(interval=0.05))
        ram = int(psutil.virtual_memory().percent)
        return cpu, ram
    except:
        return 0, 0

PAGES = [
    {
        "title": "MALICIOUS TOOLS",
        "description": "Payload builders, DDoS, scanners and bombers",
        "tools": [
            ("01", "Make Grabber", "Compile password and token stealing payloads"),
            ("02", "Make RAT", "Build Remote Access Trojan stubs"),
            ("03", "Make IP Grabber", "Generate tracking links to log visitor IPs"),
            ("04", "Make Keylogger", "Build stealth keystroke logging applications"),
            ("05", "Crypto Wallet Scanner", "Scan for cryptocurrency wallet mnemonics"),
            ("06", "Mail Bomber", "Send spam emails to target addresses"),
            ("07", "Advanced DDoS Attack", "Perform high-traffic network stress tests"),
            ("08", "Vulnerability Scanner", "Scan targets for common web vulnerabilities"),
            ("09", "Blocker", "Block keyboard/mouse remotely via pastebin commands")
        ]
    },
    {
        "title": "DISCORD TOOLS",
        "description": "Token tools, raid, webhook, and server utilities",
        "tools": [
            ("01", "Selfbot", "Launch a custom Discord selfbot menu"),
            ("02", "Raid / Nuke Tool", "Advanced server destruction bot console"),
            ("03", "Webhook Spam", "Spam Discord webhooks with messages"),
            ("04", "Webhook Delete", "Delete Discord webhooks"),
            ("05", "Token Info", "Get information from a Discord token"),
            ("06", "Token Login", "Automated token login using Selenium"),
            ("07", "Token Nuker", "Destroy Discord accounts (chaos mode)"),
            ("08", "Token Rotator", "Rotate custom statuses on Discord accounts"),
            ("09", "Token Onliner", "Keep Discord tokens online"),
            ("10", "ID to Token", "Bruteforce Discord tokens from user ID"),
            ("11", "Server Cloner", "Clone Discord servers using a token"),
            ("12", "Server Info", "Retrieve guild information from invite link"),
            ("13", "Username Checker", "Check availability of Discord usernames"),
            ("14", "Report Bot", "Automatically report Discord messages"),
            ("15", "Bot Invite Generator", "Generate admin bot invite links"),
            ("16", "Back", "Return to main menu")
        ]
    },
    {
        "title": "OSINT & NETWORK",
        "description": "IP, DNS, whois, phone tracer, and dox trackers",
        "tools": [
            ("01", "IP Lookup", "Retrieve IP geolocation data"),
            ("02", "Email Lookup", "Retrieve OSINT data associated with emails"),
            ("03", "Phone Lookup", "Lookup carrier and location of phone numbers"),
            ("04", "Username Tracker", "Track usernames across social networks"),
            ("05", "Whois Lookup", "Retrieve domain registration details"),
            ("06", "DNS Enumeration", "Lookup target DNS records"),
            ("07", "Subdomain Finder", "Find subdomains of a target domain"),
            ("08", "Advanced Port Scanner", "Scan target hosts for open ports"),
            ("09", "Shodan Search", "Search Shodan public database"),
            ("10", "Wayback Machine", "View archived versions of websites"),
            ("11", "Social Media Scraper", "Check presence on social networks"),
            ("12", "Email Verifier", "Verify email syntax and MX records"),
            ("13", "Pastebin Dorking", "Search Pastebin for keywords"),
            ("14", "GeoIP Location", "Get geographic location from IP"),
            ("15", "Dox Creator", "Create custom doxing profiles"),
            ("16", "Back", "Return to main menu")
        ]
    },
    {
        "title": "TOOLS",
        "description": "Binder, crypter, obfuscator, and utility tools",
        "tools": [
            ("01", "Binder", "Link two executables into one"),
            ("02", "Crypter", "Obfuscate executables to avoid detection"),
            ("03", "Fusion", "Merge Grabber and RAT into one payload"),
            ("04", "Crypted RAT", "Build fully undetectable RAT"),
            ("05", "Crypted Grabber", "Build fully undetectable grabber"),
            ("06", "USB Worm", "Create autorun USB worm payload"),
            ("07", "Network Scanner", "Scan local network for connected devices"),
            ("08", "Phishing Page", "Generate phishing pages for Discord/Roblox/Steam"),
            ("09", "Proxy Scraper", "Scrape HTTP, SOCKS4, and SOCKS5 proxies"),
            ("10", "Proxy Checker", "Test scraped proxies for latency and validity"),
            ("11", "Website Cloner", "Clone HTML source code of target websites"),
            ("12", "Python Obfuscator", "Obfuscate Python code"),
            ("13", "Back", "Return to main menu")
        ]
    },
    {
        "title": "LOGIN",
        "description": "Token and cookie login utilities",
        "tools": [
            ("01", "Token Login", "Login to Discord using a token"),
            ("02", "Cookie Login", "Login to websites using cookies"),
            ("03", "Back", "Return to main menu")
        ]
    },
    {
        "title": "ROBLOX TOOLS",
        "description": "User info, cookie, group, and asset tools",
        "tools": [
            ("01", "User Info", "Get Roblox user profile information"),
            ("02", "Cookie Info", "Extract information from Roblox cookie"),
            ("03", "Cookie Login", "Automated cookie login via browser"),
            ("04", "Cookie Refresher", "Refresh Roblox cookies"),
            ("05", "Group Info", "Get information about a Roblox group"),
            ("06", "Asset Download", "Download Roblox assets"),
            ("07", "Name History", "Get username history of a Roblox user"),
            ("08", "Username Checker", "Check Roblox username availability"),
            ("09", "Generate Usernames", "Generate Roblox usernames"),
            ("10", "Back", "Return to main menu")
        ]
    },
    {
        "title": "SETTINGS",
        "description": "Application settings and configuration",
        "tools": [
            ("01", "Clear Settings", "Clear all saved settings"),
            ("02", "Back", "Return to main menu")
        ]
    }
]

CAT_SHORT = ["MALIC", "DISC", "OSINT", "TOOLS", "LOGIN", "RBLX", "SET"]

def get_theme_colors():
    return Theme.get_colors()

def draw_logo(colors):
    lines = BANNER.strip('\n').splitlines()
    for line in lines:
        if line.strip():
            print(Colorate.Horizontal(colors["banner"], Center.XCenter(line)))

def draw_tabs(active_idx, bw, colors):
    inner = bw - 2
    tabs = []
    for i, name in enumerate(CAT_SHORT):
        if i == active_idx:
            tabs.append(Colorate.Horizontal(colors["head"], f"[{name}]"))
        else:
            tabs.append(Colorate.Horizontal(colors["num"], name))
    tab_line = "  ".join(tabs)
    plain_len = len(strip_ansi(tab_line))
    pad = max(0, (inner - plain_len) // 2)
    extra = max(0, inner - plain_len - pad * 2)
    m = margin(bw)
    print(m + Colorate.Horizontal(colors["sub"], "┌" + "─" * inner + "┐"))
    print(m + Colorate.Horizontal(colors["sub"], "│") + " " * pad + tab_line + " " * pad + " " * extra + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

def draw_page_content(active_idx, bw, colors):
    page = PAGES[active_idx]
    inner = bw - 2
    title = f" {page['title']} — {page['description']} "
    if len(strip_ansi(title)) > inner:
        title = f" {page['title']} "
    bl = max(2, (inner - len(strip_ansi(title))) // 2)
    ex = "─" if (inner - len(strip_ansi(title))) % 2 else ""
    top = "┌" + "─" * bl + title + "─" * bl + ex + "┐"
    m = margin(bw)
    print(m + Colorate.Horizontal(colors["sub"], top))
    print(m + Colorate.Horizontal(colors["sub"], "├" + "─" * inner + "┤"))
    for num, name, desc in page["tools"]:
        num_part = Colorate.Horizontal(colors["num"], num)
        name_part = Colorate.Horizontal(colors["txt"], name.ljust(22))
        desc_part = Colorate.Horizontal(colors["sub"], desc)
        line = num_part + "  " + name_part + "  " + desc_part
        if len(strip_ansi(line)) > inner:
            line = line[:inner-3] + "..."
        pad = max(0, inner - len(strip_ansi(line)))
        print(m + Colorate.Horizontal(colors["sub"], "│") + line + " " * pad + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

def get_footer_lines(bw, colors):
    inner = bw - 2
    nav_items = []
    for text, key in [("[B]Back", "b"), ("[N]Next", "n"), ("[H]Help", "h"), ("[1-7]Cat", "num"), ("[Q]uit", "q")]:
        if key == "q":
            nav_items.append(Colorate.Horizontal(colors["head"], text))
        elif key == "num":
            nav_items.append(Colorate.Horizontal(colors["num"], text))
        else:
            nav_items.append(Colorate.Horizontal(colors["sub"], text))
    nav = "  " + ("  " + Colorate.Horizontal(colors["sub"], "│") + "  ").join(nav_items) + "  "
    pad = max(0, (inner - len(strip_ansi(nav))) // 2)
    extra = max(0, inner - len(strip_ansi(nav)) - pad * 2)
    line1 = " " * pad + nav + " " * pad + " " * extra

    cpu, ram = get_stats()
    cpu_text = Colorate.Horizontal(colors["num"], f"CPU {cpu:>2}%")
    ram_text = Colorate.Horizontal(colors["num"], f"RAM {ram:>2}%")
    info = f"{cpu_text}  {ram_text}"
    # Centrer la ligne
    plain_info = strip_ansi(info)
    pad_info = max(0, (inner - len(plain_info)) // 2)
    extra_info = max(0, inner - len(plain_info) - pad_info * 2)
    line2 = " " * pad_info + info + " " * pad_info + " " * extra_info

    return line1, line2

def draw_footer(bw, colors):
    m = margin(bw)
    inner = bw - 2
    line1, line2 = get_footer_lines(bw, colors)
    print(m + Colorate.Horizontal(colors["sub"], "│") + line1 + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "│") + line2 + Colorate.Horizontal(colors["sub"], "│"))
    print(m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))

def dashboard(idx):
    clr()
    colors = get_theme_colors()
    bw = box_w()
    hostname = socket.gethostname()
    ver = get_config().get("version", "1.0.0")
    header = f"SNOOP - MULTI-TOOLS v{ver}  User: {hostname}"
    print(Colorate.Horizontal(colors["head"], Center.XCenter(header)))
    draw_logo(colors)
    print()
    draw_tabs(idx, bw, colors)
    print()
    draw_page_content(idx, bw, colors)
    print()
    draw_footer(bw, colors)

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
            colors = get_theme_colors()
            bw = box_w()
            line1, line2 = get_footer_lines(bw, colors)
            m = margin(bw)
            inner = bw - 2
            sys.stdout.write("\033[2A")  # go up 2 lines
            sys.stdout.write("\r" + m + Colorate.Horizontal(colors["sub"], "│") + line1 + Colorate.Horizontal(colors["sub"], "│"))
            sys.stdout.write("\033[1B")  # down 1
            sys.stdout.write("\r" + m + Colorate.Horizontal(colors["sub"], "│") + line2 + Colorate.Horizontal(colors["sub"], "│"))
            sys.stdout.write("\033[1B")  # down 1
            sys.stdout.write("\r" + m + Colorate.Horizontal(colors["sub"], "└" + "─" * inner + "┘"))
            sys.stdout.flush()
            continue

        if key in ("q", "\x1b"):
            clr()
            print(Colorate.Horizontal(Colors.purple, "SNOOP terminated."))
            break
        elif key in ("\r", "\n", " "):
            print()
            print(Colorate.Horizontal(Colors.purple, "  -> " + PAGES[idx]["title"] + " selected"))
            time.sleep(0.2)
            input(Colorate.Horizontal(Colors.cyan, "  Press Enter to return..."))
            dashboard(idx)
        elif key == "h":
            clr()
            m = " " * max(0, (term_w() - 80) // 2)
            help_lines = [
                "██╗  ██╗███████╗██╗     ██████╗",
                "██║  ██║██╔════╝██║     ██╔══██╗",
                "███████║█████╗  ██║     ██████╔╝",
                "██╔══██║██╔══╝  ██║     ██╔═══╝",
                "██║  ██║███████╗███████╗██║",
                "╚═╝  ╚═╝╚══════╝╚══════╝╚═╝"
            ]
            for line in help_lines:
                print(m + Colorate.Horizontal(Colors.purple, line))
            print()
            print(m + Colorate.Horizontal(Colors.cyan, "Navigation:"))
            print(m + "  " + Colorate.Horizontal(Colors.blue, "<-") + "/" + Colorate.Horizontal(Colors.blue, "->") + " or " +
                  Colorate.Horizontal(Colors.blue, "B") + "/" + Colorate.Horizontal(Colors.blue, "N") + "  : Change category")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "Enter") + "     : Select tool")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "Q") + "        : Quit")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "H") + "        : This help")
            print()
            print(m + Colorate.Horizontal(Colors.cyan, "Categories:"))
            print(m + "  " + Colorate.Horizontal(Colors.blue, "1") + " - MALICIOUS TOOLS    " +
                  Colorate.Horizontal(Colors.blue, "5") + " - LOGIN")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "2") + " - DISCORD TOOLS      " +
                  Colorate.Horizontal(Colors.blue, "6") + " - ROBLOX TOOLS")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "3") + " - OSINT & NETWORK    " +
                  Colorate.Horizontal(Colors.blue, "7") + " - SETTINGS")
            print(m + "  " + Colorate.Horizontal(Colors.blue, "4") + " - TOOLS")
            print()
            print(m + Colorate.Horizontal(Colors.purple, "<< Purple Phantom >>"))
            print()
            input(Colorate.Horizontal(Colors.cyan, "  Press Enter to continue..."))
            dashboard(idx)
        elif key == "r":
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
        draw_page_content(active_idx, bw, colors)

    @classmethod
    def draw_header(cls, colors, bw, m):
        pass

    @classmethod
    def draw_footer(cls, colors, bw, m):
        draw_footer(bw, colors)

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

if __name__ == "__main__":
    try:
        if term_w() < 60:
            print(Colorate.Horizontal(Colors.red, "Error: Terminal too small."))
            sys.exit(1)
        run()
    except KeyboardInterrupt:
        clr()
        print()
        print(Colorate.Horizontal(Colors.purple, "SNOOP terminated."))
        sys.exit(0)
