#!/usr/bin/env python3
# SNOOP Python Obfuscator – obfusque un script Python

import os, zlib, base64, marshal, time, tkinter as tk
from tkinter import filedialog
from colorama import Fore, Style, init
init(autoreset=True)

def obfuscate(code):
    compiled = compile(code, '', 'exec')
    marshaled = marshal.dumps(compiled)
    compressed = zlib.compress(marshaled)
    b64 = base64.b64encode(compressed).decode()
    reversed_b64 = b64[::-1]
    xor = "".join([chr(ord(c) ^ 0x7) for c in reversed_b64])
    hexed = xor.encode().hex()
    loader = (
        "m=__import__('marshal');z=__import__('zlib');b=__import__('base64');"
        "exec(m.loads(z.decompress(b.b64decode(''.join([chr(ord(i)^0x7) for i in bytes.fromhex('"+hexed+"').decode()[::-1]])))))"
    )
    return "'''\n~ OBFUSCATED BY SNOOP ~\n'''\n" + loader

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP PYTHON OBFUSCATOR         ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [*] Select a Python file...{Style.RESET_ALL}")
    root = tk.Tk(); root.withdraw(); root.attributes("-topmost", True)
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    root.destroy()
    if not file_path:
        print(f"{Fore.RED}  [!] No file selected.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        obf = obfuscate(code)
        os.makedirs("output", exist_ok=True)
        out_name = os.path.basename(file_path).replace(".py", "-obf.py")
        out_path = os.path.join("output", out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(obf)
        print(f"{Fore.GREEN}  [+] Obfuscated saved to: {out_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}  [!] Error: {e}{Style.RESET_ALL}")
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()