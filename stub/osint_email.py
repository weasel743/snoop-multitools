#!/usr/bin/env python3
# OSINT: Email Lookup (via emailrep.io – public, sans clé)

import sys
import requests

def lookup(email):
    try:
        # emailrep.io est gratuit et ne nécessite pas de clé pour une utilisation limitée
        r = requests.get(f"https://emailrep.io/{email}", timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n[SNOOP OSINT] Email Lookup")
    email = input("Enter email address: ").strip()
    if not email:
        print("[!] Email required.")
        input("Press Enter...")
        return
    print(f"\n[+] Looking up {email}...")
    data = lookup(email)
    if "error" in data:
        print(f"[!] Error: {data['error']}")
    else:
        print(f"Reputation: {data.get('reputation', 'N/A')}")
        print(f"Suspicious: {data.get('suspicious', 'N/A')}")
        print(f"Malicious: {data.get('malicious', 'N/A')}")
        details = data.get('details', {})
        if details:
            print("Details:")
            for k, v in details.items():
                print(f"  {k}: {v}")
        if 'references' in data:
            print(f"References count: {len(data['references'])}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()