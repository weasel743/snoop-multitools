#!/usr/bin/env python3
# OSINT: Wayback Machine Snapshot (archives d'un site)

import sys
import requests
import json

def get_wayback(url):
    try:
        api = f"https://archive.org/wayback/available?url={url}"
        r = requests.get(api, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("\n[SNOOP OSINT] Wayback Machine Snapshot")
    url = input("Enter URL (e.g., example.com): ").strip()
    if not url:
        print("[!] URL required.")
        input("Press Enter...")
        return
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\n[+] Checking archives for {url}...")
    data = get_wayback(url)
    if "error" in data:
        print(f"[!] Error: {data['error']}")
    else:
        archived_snapshots = data.get('archived_snapshots', {})
        if archived_snapshots:
            closest = archived_snapshots.get('closest', {})
            if closest:
                print(f"Available snapshot: {closest.get('url', 'N/A')}")
                print(f"Timestamp: {closest.get('timestamp', 'N/A')}")
                print(f"Status: {closest.get('status', 'N/A')}")
            else:
                print("No snapshot found.")
        else:
            print("No archived snapshots.")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()