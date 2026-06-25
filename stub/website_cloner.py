#!/usr/bin/env python3
# SNOOP Website Cloner – clone un site web statique

import os, requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP WEBSITE CLONER            ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")
    url = input(f"{Fore.CYAN}  URL (ex: example.com): {Style.RESET_ALL}").strip()
    if not url:
        print(f"{Fore.RED}  [!] URL required.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    if not url.startswith("http"):
        url = "https://" + url
    print(f"{Fore.GREEN}  [*] Cloning {url}...{Style.RESET_ALL}")
    try:
        base = "/".join(url.split("/")[:3])
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, timeout=10, headers=headers)
        if r.status_code != 200:
            print(f"{Fore.RED}  [!] Status: {r.status_code}{Style.RESET_ALL}")
            input("  Press Enter...")
            return
        soup = BeautifulSoup(r.text, "html.parser")
        safe = url.split("//")[-1].replace("/", "_").replace(".", "_")
        out_dir = os.path.join("output", f"clone_{safe}")
        for d in ["css", "js", "img"]:
            os.makedirs(os.path.join(out_dir, d), exist_ok=True)
        # Download linked resources
        for tag, attr, folder in [("img","src","img"), ("link","href","css"), ("script","src","js")]:
            for el in soup.find_all(tag):
                val = el.get(attr)
                if val:
                    if val.startswith("//"):
                        src = "https:" + val
                    elif val.startswith("/"):
                        src = base + val
                    elif not val.startswith("http"):
                        src = url + "/" + val
                    else:
                        src = val
                    try:
                        name = src.split("/")[-1].split("?")[0]
                        if not name: continue
                        if folder == "css" and not name.endswith(".css"): continue
                        res = requests.get(src, timeout=5)
                        path = os.path.join(out_dir, folder, name)
                        with open(path, "wb") as f:
                            f.write(res.content)
                        el[attr] = os.path.join(folder, name)
                    except: pass
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"{Fore.GREEN}  [+] Cloned successfully! Folder: {out_dir}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}  [!] Error: {e}{Style.RESET_ALL}")
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()