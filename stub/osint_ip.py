#!/usr/bin/env python3
# OSINT: IP Lookup & Geolocation (sans clé)

import sys
import json
import requests

def get_own_ip():
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=5)
        return r.json().get('ip')
    except:
        return None

def lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,proxy,hosting", timeout=10)
        return r.json()
    except Exception as e:
        return {"status":"fail", "message":str(e)}

def main():
    print("\n[SNOOP OSINT] IP Lookup & Geolocation")
    target = input("Enter IP address (or leave empty for your own): ").strip()
    if not target:
        target = get_own_ip()
        if not target:
            print("[!] Could not retrieve your own IP.")
            input("Press Enter...")
            return
    print(f"\n[+] Looking up IP: {target}")
    data = lookup(target)
    if data.get('status') == 'fail':
        print(f"[!] Error: {data.get('message', 'Unknown')}")
    else:
        print(f"Country: {data.get('country', 'N/A')}")
        print(f"Region: {data.get('regionName', 'N/A')}")
        print(f"City: {data.get('city', 'N/A')}")
        print(f"ZIP: {data.get('zip', 'N/A')}")
        print(f"ISP: {data.get('isp', 'N/A')}")
        print(f"Org: {data.get('org', 'N/A')}")
        print(f"AS: {data.get('as', 'N/A')}")
        print(f"Timezone: {data.get('timezone', 'N/A')}")
        print(f"Proxy/VPN: {'Yes' if data.get('proxy') else 'No'}")
        print(f"Hosting: {'Yes' if data.get('hosting') else 'No'}")
        print(f"Coordinates: {data.get('lat')}, {data.get('lon')}")
        print(f"Map: https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()