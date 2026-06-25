#!/usr/bin/env python3
# OSINT: DNS Enumeration (A, MX, NS, TXT, etc.)

import sys
import dns.resolver

def query(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(r) for r in answers]
    except Exception as e:
        return [f"Error: {e}"]

def main():
    print("\n[SNOOP OSINT] DNS Enumeration")
    domain = input("Enter domain: ").strip()
    if not domain:
        print("[!] Domain required.")
        input("Press Enter...")
        return
    print(f"\n[+] Querying DNS for {domain}...")
    for rtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
        results = query(domain, rtype)
        print(f"{rtype}: {', '.join(results) if results else 'No record'}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()