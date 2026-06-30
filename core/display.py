#!/usr/bin/env python3

import os
import sys
import time
import json
import random
import shutil
from core.themes import THEMES
from core.modern_ui import ModernUI

user = os.environ.get('USERNAME', 'Unknown') if os.name == 'nt' else os.environ.get('USER', 'Unknown')

# ============================================================================================
#  BOOT FLAG – PERMET DE N'EXÉCUTER boot_anim() QU'UNE SEULE FOIS
# ============================================================================================
_BOOT_DONE = False

def get_config():
    try:
        if os.path.exists("core/config.json"):
            with open("core/config.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {}

try:
    import pystyle
    from pystyle import Center, System
except ImportError:
    print("Please install pystyle: pip install pystyle")
    sys.exit(1)

class Colors(pystyle.Colors):
    pass

class Colorate:
    @staticmethod
    def Horizontal(color, text, *args, **kwargs):
        cfg = get_config()
        if cfg.get("theme", "snoop").lower() == "rainbow":
            return pystyle.Colorate.Horizontal(pystyle.Colors.rainbow, text, *args, **kwargs)
        if isinstance(color, str):
            return f"{color}{text}{pystyle.Colors.reset}"
        return pystyle.Colorate.Horizontal(color, text, *args, **kwargs)

    @staticmethod
    def Vertical(color, text, *args, **kwargs):
        cfg = get_config()
        if cfg.get("theme", "snoop").lower() == "rainbow":
            return pystyle.Colorate.Vertical(pystyle.Colors.rainbow, text, *args, **kwargs)
        return pystyle.Colorate.Vertical(color, text, *args, **kwargs)

class Theme:
    @staticmethod
    def get_colors():
        c = get_config().get("theme", "snoop").lower()
        t = THEMES.get(c, THEMES["snoop"])
        return {
            "banner": t["banner"],
            "head": t["head"],
            "num": t["num"],
            "txt": t["txt"],
            "sub": t["sub"],
            "inp": t["inp"]
        }

    @staticmethod
    def get_matrix_color():
        c = get_config().get("theme", "snoop").lower()
        if c == "rainbow":
            return -1
        m = {"red":196, "purple":93, "green":46, "yellow":226, "pink":201, "cyan":51, "gray":245, "blue":27, "modern_red":196, "modern_purple":93, "snoop":93, "snoop_neon":93, "snoop_dark":93, "snoop_holo":51}
        return m.get(c, 93)

def clr():
    System.Clear()

def init_os():
    cfg = get_config()
    ver = cfg.get("version", "1.0.")
    user = os.environ.get('USERNAME', 'Unknown') if os.name == 'nt' else os.environ.get('USER', 'Unknown')
    try:
        if os.name == 'nt':
            os.system('mode con cols=120 lines=38')
            sys.stdout.write('\x1b[8;38;120t')
            sys.stdout.flush()
        else:
            sys.stdout.write('\x1b[8;38;120t')
            sys.stdout.flush()
    except:
        pass
    System.Title(f"SN00P @ {user} ~ v{ver}")
    cols, rows = shutil.get_terminal_size()
    if cols < 80:
        cl = Theme.get_colors()
        print(Colorate.Horizontal(cl.get("num", ""), f"\n  [!] Terminal width: {cols} (min 80 recommended)"))
        print(Colorate.Horizontal(cl.get("txt", ""), "      Please widen your terminal for best experience\n"))
        time.sleep(2.0)

def type_print(text, delay=0.03):
    cl = Theme.get_colors()
    sys.stdout.write(Colorate.Horizontal(cl["num"], "  [*] "))
    for c in text:
        sys.stdout.write(Colorate.Horizontal(cl["txt"], c))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

SNOOP_BANNER = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢋⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⢾⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠟⣿⢸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠠⠤⢤⣤⣤⣴⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣄⣿⣿⣾⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢹⣿⠀⠀⠀⠀⠀⣀⣠⣴⣶⡿⠿⠟⠒⠛⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠻⠿⢿⣶⣤⣄⣀⠀⠀⠘⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⠀⢀⣤⣶⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⠿⣶⣤⣿⣿⣿⣿⣟⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣾⡿⠿⠿⠿⢿⣿⣷⣶⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⢿⣿⡿⠿⠛⣿⡿⠀⠀⢀⣠⣴⣾⣿⡟⠋⠉⠀⠀⠈⢧⡀⣷⣄⡂⠙⢧⡁⡝⢿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣧⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣦⡀⠀⢀⡴⢻⣿⣴⣾⡿⣟⣉⣼⣟⠤⠤⠖⠒⠒⠒⠒⠻⢏⡛⢬⡙⠛⠳⢄⠀⠳⣍⡻⣿⣿⣿⠿⣿⣷⣶⣤⣄⣸⣿⣿⣿⣿⡏⢧⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢸⢹⠉⠀⢷⡏⢰⡟⠢⡄⢰⣶⣶⣿⣿⣿⣶⡖⠉⠢⢝⡂⠀⠀⠙⠢⢄⣙⣺⣿⣿⣷⣶⢾⡟⢻⣿⣿⣿⣿⣿⣿⠁⢈⡷⣄⢀⣀⣨⠭⠟⣩⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⡜⣼⠀⢀⠀⣇⣿⣿⣿⡿⠟⣿⣿⣿⡿⣿⢿⣎⣳⢤⣀⠈⠙⢶⡶⠤⢤⣴⣶⣶⣷⣍⣫⡾⣡⣿⠿⣜⡇⠠⢀⡏⠀⢀⢳⡈⠑⢦⣤⣴⣾⣿⣿⣿⣿
⣿⣿⣿⣦⣄⣀⣀⣀⣠⠊⡇⡏⢠⠈⠲⢿⣿⣿⣧⡀⠀⢴⣯⣙⠷⠿⠔⠊⠁⠀⠀⠉⠙⡒⠛⠦⠤⢌⣙⠋⠛⠉⠙⠛⠛⠋⠛⣼⡇⢀⣾⡇⠀⣾⡦⠽⣶⡤⣬⣭⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠿⠟⣡⡞⠁⡟⡆⢳⡀⢆⢿⠻⡑⠞⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡐⠀⢸⠲⣄⠀⠀⠀⠉⠓⠢⠤⣀⠀⣠⠞⣁⣴⣯⢏⡇⣰⣿⡇⠘⢾⡻⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢦⢱⢹⡀⠹⣌⢾⢧⠙⠦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⢸⠀⠈⡆⠀⠀⠀⠀⠀⠑⠤⣉⣙⣉⢅⡾⢃⣾⣴⢯⡇⢻⡀⢠⣙⣦⣬⣽⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣶⣶⡇⢸⡘⡄⢻⣄⠙⢿⣶⢵⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⢘⣆⣠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠰⢚⣹⢷⣿⡟⢡⣿⠁⠘⣧⡈⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣎⡇⠘⡄⠻⣷⣄⠙⠧⣄⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣼⣋⣴⡿⡼⢀⡀⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠃⠀⢨⢦⢌⣢⣙⣷⡺⣍⡉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣯⡟⢹⣿⣧⠇⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⠀⢳⣷⣌⡙⠻⢧⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠤⣔⣒⠦⠤⠄⠀⠀⠀⠀⠀⠀⢠⢯⣾⢈⢼⡟⠏⢠⢿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣦⠀⠻⡝⣿⠛⡖⣿⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣰⡞⠁⣰⢋⡞⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣷⣄⠹⣼⢯⣷⠘⣿⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⣿⣿⣿⣫⣴⢛⢳⣯⣞⣉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠙⣾⣮⣿⣤⣿⣞⣿⣷⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⢀⣿⣿⣿⣿⣾⣷⣿⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢠⣿⣿⣿⣿⣷⣿⣿⣿⣆⠈⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⠁⣠⠔⠋⣿⣿⣿⣿⣿⣿⣿⣿⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠃⠐⢋⣾⣿⣿⣿⣾⣿⣿⣿⣿⡀⠀⠀⠀⠉⠒⠤⢄⣀⣀⡠⠔⠋⣀⣠⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠉⣉⣍⣩⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣎⠉⢃⠈⣼⣿⣿⣿⣿⣿⣿⡿⠟⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠹⣿⣿⣿⣿⣦⣼⢤⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⣀⣉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡀⠀⡏⠹⡟⣿⣿⢀⡎⣽⠋⢰⠁⠀⠀⠀⠀⢀⣠⡴⠿⣛⣭⡷⠿⠛⠋⠉⠁⠀⢀⡤⣺⣷⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠘⡟⣿⣆⡇⠀⢳⣷⣿⣿⢰⠏⠀⢺⣀⠤⠴⣒⣫⣽⣶⠾⠛⠉⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⡏⠀⠀⠙⢮⣙⣷⠄⢀⣿⣿⣧⠋⠤⢒⡏⡔⢛⡉⠁⢀⠉⢀⠀⠀⠀⠀⠀⠀⠀⢀⡠⣻⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⠔⢉
                                                                      
   @@@@@@ @@@  @@@  @@@@@@   @@@@@@  @@@@@@@       @@@@@@@  @@@@@@   @@@@@@  @@@       @@@@@@
 !@@     @@!@!@@@ @@!  @@@ @@!  @@@ @@!  @@@        @@!   @@!  @@@ @@!  @@@ @@!      !@@    
  !@@!!  @!@@!!@! @!@  !@! @!@  !@! @!@@!@!         @!!   @!@  !@! @!@  !@! @!!       !@@!! 
     !:! !!:  !!! !!:  !!! !!:  !!! !!:             !!:   !!:  !!! !!:  !!! !!:          !:!
 ::.: :  ::    :   : : ::   : : ::   :               :     : :. :   : :. :  : ::.: : ::.: : 
"""

def boot_anim():
    global _BOOT_DONE
    if _BOOT_DONE:
        return
    _BOOT_DONE = True
    
    clr()
    cols = Theme.get_colors()
    
    print(Colorate.Horizontal(cols["banner"], Center.XCenter(SNOOP_BANNER)))
    print(Colorate.Horizontal(cols["sub"], Center.XCenter("\n~ SNOOP TOOLKIT v1.0 ~")))
    print("\n")
    
    # ============================================================
    # BARRE DE CHARGEMENT RAINBOW AVEC SPINNER
    # ============================================================
    
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    messages = [
        ("Booting SNOOP Core...", 0, 30),
        ("Loading modules...", 30, 60),
        ("Initializing interface...", 60, 85),
        ("System ready!", 85, 100)
    ]
    
    width = 40
    step = 0
    
    for msg, start, end in messages:
        for pct in range(start, end + 1):
            filled = int((pct / 100) * width)
            empty = width - filled
            
            # Barre rainbow
            bar = ""
            for i in range(width):
                if i < filled:
                    color = get_rainbow_color(i, width)
                    bar += f"{color}█{Colors.reset}"
                else:
                    bar += f"{Colors.dark_gray}▯{Colors.reset}"
            
            pct_color = get_rainbow_color(pct, 100)
            spin = spinner[step % len(spinner)]
            step += 1
            
            # Construction
            line = f"\r  {Colorate.Horizontal(Colors.rainbow, spin)} "
            line += bar
            line += f" {Colorate.Horizontal(Colors.rainbow, ']')}"
            line += f" {pct_color}{pct:>3}%{Colors.reset}"
            line += f"  {Colorate.Horizontal(Colors.rainbow, msg)}"
            
            sys.stdout.write(line)
            sys.stdout.flush()
            
            if pct < 30:
                time.sleep(0.035)
            elif pct < 60:
                time.sleep(0.025)
            elif pct < 85:
                time.sleep(0.02)
            else:
                time.sleep(0.04)
        
        print()
        time.sleep(0.1)
    
    print(Colorate.Horizontal(Colors.rainbow, "\n  ✦ SNOOP System initialized successfully ✦\n"))
    time.sleep(0.5)

def get_rainbow_color(value, max_value):
    hue = (value / max_value) * 360
    h = hue / 60
    i = int(h)
    f = h - i
    
    if i == 0:
        r, g, b = 1, f, 0
    elif i == 1:
        r, g, b = 1 - f, 1, 0
    elif i == 2:
        r, g, b = 0, 1, f
    elif i == 3:
        r, g, b = 0, 1 - f, 1
    elif i == 4:
        r, g, b = f, 0, 1
    else:
        r, g, b = 1, 0, 1 - f
    
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return f"\033[38;2;{r};{g};{b}m"

def matrix_effect(cycles=1, color_id=27):
    s = shutil.get_terminal_size()
    cols, rows = s.columns, s.lines
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%\"'#&_(),.;:?!\\|{}<>[]^~"
    d = [0 for _ in range(cols)]
    sys.stdout.write("\033[?25l")
    done, stps = 0, 0
    while done < cycles:
        out = "\033[H"
        for r in range(rows):
            l = ""
            for c in range(cols):
                if d[c] == r: l += "\033[38;5;15m" + random.choice(chars)
                elif d[c] > r and d[c] - 10 < r:
                    cid = random.choice([27, 196, 93, 46, 226, 201, 51]) if color_id == -1 else color_id
                    l += f"\033[38;5;{cid}m" + random.choice(chars)
                else: l += " "
            out += l + "\n"
        for i in range(cols):
            if d[i] > rows:
                d[i] = 0
                if i == 0: done += 1
            elif d[i] == 0:
                if random.random() > 0.95: d[i] = 1
            else: d[i] += 1
        sys.stdout.write(out)
        sys.stdout.flush()
        time.sleep(0.03)
        stps += 1
        if stps > (rows * cycles * 2) + 100: break
    sys.stdout.write("\033[?25h\033[0m\033[2J\033[H")

def print_banner():
    cfg = get_config()
    if cfg.get("theme", "blue").lower().startswith("modern"):
        return ModernUI.print_banner(Colorate, Theme, clr)
    clr()
    cols = Theme.get_colors()
    print(Colorate.Horizontal(cols["banner"], Center.XCenter(SNOOP_BANNER)))
    print(Colorate.Horizontal(cols["sub"], Center.XCenter("\n~ SN00P TOOLKIT v1.0 ~")))
    print("\n")

def menu_opts(options):
    cl = Theme.get_colors()
    _items = list(options.items())
    for i in range(0, len(_items), 2):
        k1, v1 = _items[i]
        _line = Colorate.Horizontal(cl["num"], f"  [{k1}] ") + Colorate.Horizontal(cl["txt"], f"{v1:<25}")
        if i + 1 < len(_items):
            k2, v2 = _items[i+1]
            _line += Colorate.Horizontal(cl["num"], f"  [{k2}] ") + Colorate.Horizontal(cl["txt"], v2)
        print(_line)
    print()

def get_inpt(prompt=None):
    cl = Theme.get_colors()
    _prmpt = f"\n  SNOOP ⚜️ > "
    return input(Colorate.Horizontal(cl["inp"], _prmpt))