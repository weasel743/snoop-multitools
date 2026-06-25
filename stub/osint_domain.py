#!/usr/bin/env python3
# OSINT: Domain Whois Lookup (utilise la librairie whois)

import sys
import whois

def lookup(domain):
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n[SNOOP OSINT] Domain Whois Lookup")
    domain = input("Enter domain (e.g., example.com): ").strip()
    if not domain:
        print("[!] Domain required.")
        input("Press Enter...")
        return
    print(f"\n[+] Querying whois for {domain}...")
    data = lookup(domain)
    if isinstance(data, dict) and "error" in data:
        print(f"[!] Error: {data['error']}")
    else:
        print(f"Domain: {data.domain_name if hasattr(data, 'domain_name') else 'N/A'}")
        print(f"Registrar: {data.registrar if hasattr(data, 'registrar') else 'N/A'}")
        print(f"Creation Date: {data.creation_date if hasattr(data, 'creation_date') else 'N/A'}")
        print(f"Expiration Date: {data.expiration_date if hasattr(data, 'expiration_date') else 'N/A'}")
        print(f"Name Servers: {data.name_servers if hasattr(data, 'name_servers') else 'N/A'}")
        print(f"Emails: {data.emails if hasattr(data, 'emails') else 'N/A'}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()