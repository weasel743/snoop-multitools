#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SNOOP OSINT – Advanced Port Scanner (SYN/Connect, service detection, banner grab)

import socket
import threading
import sys
import os
import time
import struct
import ipaddress
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

# Dictionnaire des services connus avec leurs ports
SERVICES = {
    20: "FTP-data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP",
    110: "POP3", 111: "RPC", 135: "MSRPC", 137: "NetBIOS-NS",
    138: "NetBIOS-DGM", 139: "NetBIOS-SSN", 143: "IMAP", 161: "SNMP",
    162: "SNMP-Trap", 179: "BGP", 389: "LDAP", 443: "HTTPS",
    445: "SMB", 465: "SMTPS", 514: "Syslog", 515: "LPD",
    587: "SMTP-Submit", 636: "LDAPS", 873: "RSYNC", 993: "IMAPS",
    995: "POP3S", 1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle",
    1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 6667: "IRC", 8000: "HTTP-Alt",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 8888: "HTTP-Alt",
    9000: "Sonar", 9200: "Elasticsearch", 27017: "MongoDB"
}

# Ports rapides (top 100)
RAPID_PORTS = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1080,1433,1521,1723,3306,3389,5432,5900,6379,8080,8443,8888,9000,9200,27017]

def resolve(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

def check_syn(ip, port, timeout=0.5):
    """Vérifie un port avec un socket raw (SYN) – nécessite admin"""
    # Sur Windows, les sockets bruts nécessitent des privilèges admin.
    # On utilise une approche TCP Connect si SYN échoue.
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.settimeout(timeout)
        # Construction d'un paquet SYN simplifié
        # (Non implémenté ici – retourne False pour utiliser Connect)
        return None
    except PermissionError:
        return None
    except:
        return None

def scan_port_tcp(ip, port, timeout=0.5):
    """Scan TCP Connect classique"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return True
        return False
    except:
        return False

def grab_banner(ip, port, timeout=2):
    """Récupère la bannière d'un service (si possible)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        if port in (80, 8080, 8000, 8888):
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        elif port == 21:
            # FTP – on attend le message de bienvenue
            pass
        elif port == 22:
            # SSH – on attend la version
            pass
        elif port == 25:
            # SMTP
            pass
        elif port == 110:
            # POP3
            pass
        elif port == 143:
            # IMAP
            pass
        else:
            # Pour les autres, on envoie un simple CRLF
            s.send(b"\r\n")
        banner = s.recv(512).decode(errors='ignore').strip()
        s.close()
        if banner:
            return banner
        return None
    except:
        return None

def scan_ports(ip, port_list, threads=100, timeout=0.5):
    """Multi-threaded port scanner"""
    results = []
    lock = threading.Lock()
    total = len(port_list)
    scanned = 0

    def worker(ports):
        nonlocal scanned
        for p in ports:
            open_status = scan_port_tcp(ip, p, timeout)
            if open_status:
                service = SERVICES.get(p, "Unknown")
                banner = grab_banner(ip, p) if open_status else None
                with lock:
                    results.append((p, service, banner))
            with lock:
                scanned += 1
                if scanned % 50 == 0:
                    sys.stdout.write(f"\r  {Fore.CYAN}Scanned: {scanned}/{total} ports{Style.RESET_ALL}")
                    sys.stdout.flush()
        # Effacer la ligne
        sys.stdout.write("\r" + " " * 50 + "\r")

    # Découpage en chunks
    chunk_size = max(1, len(port_list) // threads)
    chunks = [port_list[i:i+chunk_size] for i in range(0, len(port_list), chunk_size)]

    threads_list = []
    for chunk in chunks:
        t = threading.Thread(target=worker, args=(chunk,))
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    results.sort()
    return results

def full_scan(target_ip):
    """Scan complet 1-65535"""
    print(f"{Fore.CYAN}[*] Scanning all ports (1-65535) – this may take a while...{Style.RESET_ALL}")
    return scan_ports(target_ip, list(range(1, 65536)), threads=200, timeout=0.3)

def rapid_scan(target_ip):
    """Scan rapide des ports communs"""
    print(f"{Fore.CYAN}[*] Rapid scan on common ports...{Style.RESET_ALL}")
    return scan_ports(target_ip, RAPID_PORTS, threads=50, timeout=0.5)

def custom_scan(target_ip, port_spec):
    """Scan avec spécification personnalisée (ex: 22,80,443 ou 1-1000)"""
    ports = []
    for part in port_spec.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end+1))
        else:
            try:
                ports.append(int(part))
            except:
                pass
    if not ports:
        print(f"{Fore.RED}[!] Aucun port valide.{Style.RESET_ALL}")
        return []
    print(f"{Fore.CYAN}[*] Scanning {len(ports)} ports...{Style.RESET_ALL}")
    return scan_ports(target_ip, ports, threads=100, timeout=0.4)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║     SNOOP PORT SCANNER – OSINT v1.0     ║")
    print("  ╚══════════════════════════════════════════╝")
    print(Style.RESET_ALL)

    target = input(f"{Fore.CYAN}  Target (IP or domain): {Style.RESET_ALL}").strip()
    if not target:
        print(f"{Fore.RED}[!] Target required.{Style.RESET_ALL}")
        input("Press Enter to return...")
        return

    ip = resolve(target)
    if not ip:
        ip = target  # fallback
        print(f"{Fore.YELLOW}[!] Could not resolve, using {ip}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[+] Resolved: {target} → {ip}{Style.RESET_ALL}")

    rev = reverse_dns(ip)
    if rev and rev != ip:
        print(f"{Fore.GREEN}[+] Reverse DNS: {rev}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}  Choose scan type:")
    print("  [1] Rapid (top 30 ports)")
    print("  [2] Full (1-65535) – can take several minutes")
    print("  [3] Custom (e.g., 22,80,443 or 1-1000)")
    choice = input(f"{Fore.MAGENTA}  Choice: {Style.RESET_ALL}").strip()

    start_time = time.time()
    if choice == "1":
        results = rapid_scan(ip)
    elif choice == "2":
        results = full_scan(ip)
    elif choice == "3":
        spec = input(f"{Fore.CYAN}  Port specification: {Style.RESET_ALL}").strip()
        results = custom_scan(ip, spec) if spec else []
    else:
        print(f"{Fore.RED}[!] Invalid choice.{Style.RESET_ALL}")
        input("Press Enter...")
        return

    elapsed = time.time() - start_time
    print(f"\n{Fore.GREEN}[+] Scan completed in {elapsed:.2f}s{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  {'─'*60}{Style.RESET_ALL}")

    if results:
        print(f"{Fore.GREEN}  Open ports:{Style.RESET_ALL}")
        for port, service, banner in results:
            line = f"  {port:5}  {service:12}"
            if banner:
                line += f"  Banner: {banner[:50]}"
            print(line)
        # Exportation des résultats
        export = input(f"\n{Fore.CYAN}  Export results to file? (y/n): {Style.RESET_ALL}").strip().lower()
        if export == 'y':
            filename = f"scan_{ip}_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                f.write(f"Scan results for {ip} ({target})\n")
                f.write(f"Open ports: {len(results)}\n")
                for port, service, banner in results:
                    f.write(f"{port} {service} {banner or ''}\n")
            print(f"{Fore.GREEN}[+] Results saved to {filename}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}  No open ports found.{Style.RESET_ALL}")

    input(f"\n{Fore.CYAN}Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()