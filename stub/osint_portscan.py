#!/usr/bin/env python3
# OSINT: Light Port Scanner

import sys
import socket
import threading
import time

COMMON_PORTS = [21,22,23,25,53,80,110,135,139,143,443,445,3306,3389,5432,5900,8080]

def scan_port(ip, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            results.append(port)
        sock.close()
    except:
        pass

def main():
    print("\n[SNOOP OSINT] Light Port Scanner")
    target = input("Enter IP address or hostname: ").strip()
    if not target:
        print("[!] Target required.")
        input("Press Enter...")
        return
    try:
        ip = socket.gethostbyname(target)
    except:
        print("[!] Invalid hostname.")
        input("Press Enter...")
        return
    print(f"\n[+] Scanning {ip} on common ports...")
    results = []
    threads = []
    for port in COMMON_PORTS:
        t = threading.Thread(target=scan_port, args=(ip, port, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    if results:
        print("Open ports:")
        for p in sorted(results):
            print(f"  {p}")
    else:
        print("No open common ports found.")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()