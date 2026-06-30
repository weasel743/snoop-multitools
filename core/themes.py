from pystyle import Colors

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

THEMES = {
    "snoop": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "snoop_neon": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "snoop_dark": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "snoop_holo": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "purple": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "blue": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "cyan": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "pink": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
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
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "modern_red": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    },
    "modern_purple": {
        "banner": Colors.rainbow,
        "head": Colors.rainbow,
        "num": Colors.rainbow,
        "txt": Colors.white,
        "sub": Colors.rainbow,
        "inp": Colors.rainbow
    }
}

DEFAULT_THEME = "rainbow"

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