#!/usr/bin/env python3
# OSINT: Subdomain Finder (dictionnaire intégré)

import sys
import dns.resolver
import requests

SUBDOMAIN_LIST = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
    "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
    "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
    "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
    "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
    "web", "media", "email", "images", "img", "download", "dns", "piwik", "stats",
    "dashboard", "portal", "manage", "start", "help", "js", "css", "cdn", "cloud"
]

def check_subdomain(domain, sub):
    fqdn = f"{sub}.{domain}"
    try:
        dns.resolver.resolve(fqdn, 'A')
        return fqdn
    except:
        return None

def main():
    print("\n[SNOOP OSINT] Subdomain Finder")
    domain = input("Enter domain: ").strip()
    if not domain:
        print("[!] Domain required.")
        input("Press Enter...")
        return
    print(f"\n[+] Scanning for subdomains of {domain}...")
    found = []
    for sub in SUBDOMAIN_LIST:
        res = check_subdomain(domain, sub)
        if res:
            found.append(res)
            print(f"[+] Found: {res}")
    if not found:
        print("No subdomains found.")
    print(f"\nTotal subdomains found: {len(found)}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()