
from pystyle import Colors

# ── SNOOP PALETTE ──
PURPLE1 = "\033[38;2;80;0;180m"
PURPLE2 = "\033[38;2;130;0;220m"
PURPLE3 = "\033[38;2;180;50;255m"
PURPLE4 = "\033[38;2;200;50;255m"
PURPLE5 = "\033[38;2;220;100;255m"

CYAN1 = "\033[38;2;0;150;200m"
CYAN2 = "\033[38;2;0;200;230m"
CYAN3 = "\033[38;2;0;230;255m"
CYAN4 = "\033[38;2;0;255;255m"

MAGENTA1 = "\033[38;2;180;0;180m"
MAGENTA2 = "\033[38;2;220;0;220m"
MAGENTA3 = "\033[38;2;255;0;255m"

WHITE = "\033[38;2;240;240;240m"
GRAY = "\033[38;2;150;150;150m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ── THEMES SNOOP ──
THEMES = {
    "snoop": {
        "banner": Colors.blue_to_purple,
        "head": Colors.purple_to_blue,
        "num": Colors.blue_to_purple,
        "txt": Colors.white,
        "sub": Colors.purple_to_blue,
        "inp": Colors.purple_to_blue
    },
    "snoop_neon": {
        "banner": Colors.purple_to_red,
        "head": Colors.blue_to_purple,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.purple_to_red,
        "inp": Colors.blue_to_purple
    },
    "snoop_dark": {
        "banner": Colors.black_to_white,
        "head": Colors.blue_to_purple,
        "num": Colors.blue_to_purple,
        "txt": Colors.white,
        "sub": Colors.purple_to_blue,
        "inp": Colors.blue_to_purple
    },
    "snoop_holo": {
        "banner": Colors.cyan_to_blue,
        "head": Colors.blue_to_cyan,
        "num": Colors.cyan_to_blue,
        "txt": Colors.white,
        "sub": Colors.blue_to_cyan,
        "inp": Colors.cyan_to_blue
    },
    "purple": {
        "banner": Colors.blue_to_purple,
        "head": Colors.purple_to_blue,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.purple_to_blue,
        "inp": Colors.purple_to_blue
    },
    "blue": {
        "banner": Colors.white_to_blue,
        "head": Colors.blue_to_cyan,
        "num": Colors.cyan_to_blue,
        "txt": Colors.white_to_blue,
        "sub": Colors.blue_to_cyan,
        "inp": Colors.blue_to_cyan
    },
    "cyan": {
        "banner": Colors.cyan_to_blue,
        "head": Colors.blue_to_cyan,
        "num": Colors.cyan,
        "txt": Colors.white,
        "sub": Colors.cyan,
        "inp": Colors.cyan
    },
    "pink": {
        "banner": Colors.purple_to_red,
        "head": Colors.red_to_purple,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.pink,
        "inp": Colors.pink
    },
    "rainbow": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "modern": {
        "banner": Colors.blue_to_purple,
        "head": Colors.purple_to_blue,
        "num": Colors.blue_to_purple,
        "txt": Colors.white_to_blue,
        "sub": Colors.purple_to_blue,
        "inp": Colors.blue_to_purple
    },
    "modern_red": {
        "banner": Colors.red_to_purple,
        "head": Colors.purple_to_red,
        "num": Colors.red_to_purple,
        "txt": Colors.white,
        "sub": Colors.red_to_purple,
        "inp": Colors.red_to_purple
    },
    "modern_purple": {
        "banner": Colors.purple_to_blue,
        "head": Colors.blue_to_purple,
        "num": Colors.purple_to_blue,
        "txt": Colors.white,
        "sub": Colors.blue_to_purple,
        "inp": Colors.purple_to_blue
    }
}

DEFAULT_THEME = "snoop"

def get_theme_colors(theme_name=None):
    if theme_name is None:
        theme_name = DEFAULT_THEME
    t = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
    return {
        "banner": t["banner"],
        "head": t["head"],
        "num": t["num"],
        "txt": t["txt"],
        "sub": t["sub"],
        "inp": t["inp"]
    }

def get_available_themes():
    return list(THEMES.keys())