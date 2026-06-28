import sys
import os
import subprocess
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
STUB_DIR = BASE_DIR / "stub"
sys.path.insert(0, str(STUB_DIR))

from core.display import clr, get_inpt, boot_anim, init_os
from core.paginated_ui import PaginatedUI, PAGES

def launch_tool(tool_name):
    script = STUB_DIR / tool_name
    if script.exists():
        try:
            subprocess.run([sys.executable, str(script)], check=True)
        except Exception as e:
            print(f"[!] Error: {e}")
            input("Press Enter...")
    else:
        print(f"[!] {tool_name} not found in stub/")
        input("Press Enter...")

def run_app():
    boot_anim()
    current_page = 0
    
    while True:
        PaginatedUI.draw_dashboard(current_page)
        choice = get_inpt().strip().lower()
        
        if choice in ("n", "d"):
            current_page = (current_page + 1) % len(PAGES)
            continue
        elif choice in ("b", "a"):
            current_page = (current_page - 1) % len(PAGES)
            continue
        elif choice == "e":
            clr()
            print("Goodbye.")
            break
        elif choice in ("1", "2", "3", "4", "5", "6", "7"):
            current_page = int(choice) - 1
            continue
        elif not choice:
            continue
        
        if current_page == 0:
            launch_tool("base_code.py")
        elif current_page == 1:
            launch_tool("discord_selfbot.py")
        elif current_page == 2:
            launch_tool("osint_ip.py")
        elif current_page == 3:
            launch_tool("binder_template.py")
        elif current_page == 4:
            launch_tool("discord_tools.py")
        elif current_page == 5:
            launch_tool("roblox.py")
        else:
            print("[!] Invalid page.")
            input("Press Enter...")

if __name__ == '__main__':
    init_os()
    run_app()
