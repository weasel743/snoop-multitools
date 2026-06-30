#!/usr/bin/env python3
import sys
import os
import requests
import json

SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")

def shodan_search_with_key(query, key):
    try:
        url = f"https://api.shodan.io/shodan/host/search?key={key}&query={query}&size=10"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def shodan_search_public(query):
    try:
        url = f"https://www.shodan.io/search?query={query}"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            return {"html": r.text[:500]}
        return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n[SNOOP OSINT] Shodan Search")
    query = input("Enter search query (e.g., 'apache'): ").strip()
    if not query:
        print("[!] Query required.")
        input("Press Enter...")
        return
    print(f"\n[+] Searching Shodan for '{query}'...")
    if SHODAN_API_KEY:
        print("[*] Using API key")
        data = shodan_search_with_key(query, SHODAN_API_KEY)
        if "error" in data:
            print(f"[!] API Error: {data['error']}")
            print("[*] Falling back to public search...")
            data = shodan_search_public(query)
        if "error" not in data:
            if "matches" in data:
                print(f"Total results: {data.get('total', 0)}")
                for i, match in enumerate(data.get('matches', [])[:5], 1):
                    print(f"\n{i}. {match.get('ip_str', 'N/A')}:{match.get('port', 'N/A')}")
                    print(f"   Hostnames: {', '.join(match.get('hostnames', []))}")
                    print(f"   Org: {match.get('org', 'N/A')}")
                    print(f"   Data: {match.get('data', '')[:100]}...")
            else:
                print("Results (raw HTML, first 500 chars):")
                print(data.get('html', '')[:500])
        else:
            print(f"[!] Error: {data['error']}")
    else:
        print("[!] No API key found. Set SHODAN_API_KEY environment variable for full access.")
        print("[*] Using public search (limited)...")
        data = shodan_search_public(query)
        if "error" in data:
            print(f"[!] Error: {data['error']}")
        else:
            print("Results (raw HTML, first 500 chars):")
            print(data.get('html', '')[:500])
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()