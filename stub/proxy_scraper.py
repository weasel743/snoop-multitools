#!/usr/bin/env python3
# SNOOP Proxy Scraper – scrapes HTTP/SOCKS proxies

import os, requests, threading, time
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP PROXY SCRAPER            ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [1] Scrape HTTP Proxies{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [2] Scrape SOCKS4 Proxies{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [3] Scrape SOCKS5 Proxies{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  [4] Scrape All (HTTP, SOCKS4, SOCKS5){Style.RESET_ALL}")
    choice = input(f"{Fore.YELLOW}  Choice (1-4): {Style.RESET_ALL}").strip()
    if choice == "5": return
    protocols = []
    if choice == "1": protocols = ["http"]
    elif choice == "2": protocols = ["socks4"]
    elif choice == "3": protocols = ["socks5"]
    elif choice == "4": protocols = ["http", "socks4", "socks5"]
    else:
        print(f"{Fore.RED}  [!] Invalid option.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    prefix = input(f"{Fore.CYAN}  Include protocol prefix? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
    print(f"{Fore.GREEN}  [*] Scraping proxies...{Style.RESET_ALL}")
    sources = {
        "http": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/http.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt"
        ],
        "socks4": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/socks4.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks4.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/socks4.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/socks4.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks4.txt"
        ],
        "socks5": [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=yes&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
            "https://raw.githubusercontent.com/hookzof/socks5_list/master/socks5.txt",
            "https://raw.githubusercontent.com/clketc/Free-Proxy-List/main/socks5.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/OfficialPutu/free-proxy/main/socks5.txt",
            "https://raw.githubusercontent.com/saisuiu/Free-Proxy-List/main/socks5.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt"
        ]
    }
    scraped = []
    lock = threading.Lock()
    def fetch(proto, url):
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                count = 0
                for line in r.text.split('\n'):
                    line = line.strip()
                    if ":" in line and not line.startswith("#"):
                        # remove any scheme prefix if present
                        for p in ["http://","https://","socks4://","socks5://"]:
                            if line.lower().startswith(p):
                                line = line[len(p):]
                        formatted = f"{proto}://{line}" if prefix else line
                        with lock:
                            scraped.append(formatted)
                            count += 1
                print(f"{Fore.GREEN}  [+] Fetched {count} from {url[:60]}...{Style.RESET_ALL}")
        except: pass
    threads = []
    for proto in protocols:
        for url in sources[proto]:
            t = threading.Thread(target=fetch, args=(proto, url))
            t.start(); threads.append(t)
    for t in threads: t.join()
    unique = list(set(scraped))
    os.makedirs("input", exist_ok=True)
    out = "input/proxies.txt"
    with open(out, "w", encoding="utf-8") as f:
        for p in unique: f.write(p + "\n")
    print(f"{Fore.GREEN}  [+] Scraped {len(scraped)} total, {len(unique)} unique saved to {out}{Style.RESET_ALL}")
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()