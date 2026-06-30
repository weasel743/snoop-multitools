#!/usr/bin/env python3
import sys
import requests
import re
import json

def lookup_emailrep(email):
    try:
        r = requests.get(f"https://emailrep.io/{email}", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def lookup_hunter(email):
    try:
        r = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("data"):
                return {"reputation": data["data"].get("score", "N/A"), "source": "hunter.io"}
        return None
    except:
        return None

def lookup_verifyemail(email):
    try:
        r = requests.get(f"https://verifyemail.org/api/v1/verify?email={email}", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            data = r.json()
            return {"reputation": data.get("status", "N/A"), "source": "verifyemail.org"}
        return None
    except:
        return None

def lookup(email):
    result = lookup_emailrep(email)
    if result and "error" not in result:
        return {"source": "emailrep.io", "data": result}
    result = lookup_hunter(email)
    if result:
        return {"source": "hunter.io", "data": result}
    result = lookup_verifyemail(email)
    if result:
        return {"source": "verifyemail.org", "data": result}
    return {"error": "All API services failed. Try again later."}

def main():
    print("\n[SNOOP OSINT] Email Lookup")
    email = input("Enter email address: ").strip()
    if not email:
        print("[!] Email required.")
        input("Press Enter...")
        return
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        print("[!] Invalid email format.")
        input("Press Enter...")
        return
    print(f"\n[+] Looking up {email}...")
    data = lookup(email)
    if "error" in data:
        print(f"[!] Error: {data['error']}")
    else:
        print(f"Source: {data.get('source', 'Unknown')}")
        result = data.get('data', {})
        if data.get('source') == 'emailrep.io':
            print(f"Reputation: {result.get('reputation', 'N/A')}")
            print(f"Suspicious: {result.get('suspicious', 'N/A')}")
            print(f"Malicious: {result.get('malicious', 'N/A')}")
            details = result.get('details', {})
            if details:
                print("Details:")
                for k, v in details.items():
                    print(f"  {k}: {v}")
            if 'references' in result:
                print(f"References count: {len(result['references'])}")
        else:
            for k, v in result.items():
                print(f"{k}: {v}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()