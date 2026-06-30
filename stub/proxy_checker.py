#!/usr/bin/env python3
# SNOOP Proxy Checker – vérifie la validité des proxies

import os, threading, time, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
init(autoreset=True)

def check_proxy(proxy, url, timeout, lock, working):
    try:
        clean = proxy.strip()
        scheme = "http"
        for s in ["http://", "https://", "socks4://", "socks5://"]:
            if clean.lower().startswith(s):
                scheme = s[:-3]
                clean = clean[len(s):]
        parts = clean.split(":")
        if len(parts) == 4:
            if parts[1].isdigit():
                ip, port, user, password = parts
            else:
                user, password, ip, port = parts
            clean = f"{user}:{password}@{ip}:{port}"
        proxy_url = f"{scheme}://{clean}"
        proxies = {"http": proxy_url, "https": proxy_url}
        start = time.time()
        r = requests.get(url, proxies=proxies, timeout=timeout, stream=True)
        elapsed = int((time.time() - start) * 1000)
        if 200 <= r.status_code < 500:
            with lock:
                print(f"{Fore.GREEN}  [+] Working: {proxy} ({elapsed}ms){Style.RESET_ALL}")
                working.append(proxy)
            return True
        else:
            with lock:
                print(f"{Fore.RED}  [-] Failed ({r.status_code}): {proxy}{Style.RESET_ALL}")
            return False
    except:
        with lock:
            print(f"{Fore.RED}  [-] Bad: {proxy}{Style.RESET_ALL}")
        return False

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP PROXY CHECKER             ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")
    proxies_file = "input/proxies.txt"
    if not os.path.exists(proxies_file):
        print(f"{Fore.RED}  [!] proxies.txt not found in input/{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    with open(proxies_file, "r", encoding="utf-8") as f:
        proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    if not proxies:
        print(f"{Fore.RED}  [!] No proxies found.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    print(f"{Fore.GREEN}  [+] Loaded {len(proxies)} proxies.{Style.RESET_ALL}")
    url = input(f"{Fore.CYAN}  Test URL (default https://discord.com/api/v9/experiments): {Style.RESET_ALL}").strip() or "https://discord.com/api/v9/experiments"
    timeout = float(input(f"{Fore.CYAN}  Timeout (3): {Style.RESET_ALL}").strip() or 3)
    threads = int(input(f"{Fore.CYAN}  Threads (50): {Style.RESET_ALL}").strip() or 50)
    print(f"{Fore.GREEN}  [*] Checking {len(proxies)} proxies...{Style.RESET_ALL}")
    lock = threading.Lock()
    working = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = [ex.submit(check_proxy, p, url, timeout, lock, working) for p in proxies]
        for f in as_completed(futures):
            try: f.result()
            except: pass
    elapsed = (time.time() - start_time) / 60
    print(f"\n{Fore.GREEN}  [+] Working: {len(working)} / {len(proxies)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [+] Elapsed: {elapsed:.2f}m{Style.RESET_ALL}")
    if working:
        os.makedirs("output", exist_ok=True)
        with open("output/working_proxies.txt", "w") as f:
            f.write("\n".join(working) + "\n")
        print(f"{Fore.GREEN}  [+] Saved to output/working_proxies.txt{Style.RESET_ALL}")
        if input(f"{Fore.CYAN}  Replace input/proxies.txt with working proxies? (y/n): {Style.RESET_ALL}").strip().lower() == 'y':
            with open(proxies_file, "w") as f:
                f.write("\n".join(working) + "\n")
            print(f"{Fore.GREEN}  [+] Updated {proxies_file}{Style.RESET_ALL}")
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()