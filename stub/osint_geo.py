#!/usr/bin/env python3
# OSINT: GeoIP Location (via ip-api.com)

import sys
import requests

def get_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,timezone,proxy,hosting", timeout=10)
        return r.json()
    except Exception as e:
        return {"status":"fail", "message":str(e)}

def main():
    print("\n[SNOOP OSINT] GeoIP Location")
    ip = input("Enter IP address (or leave empty for your own): ").strip()
    if not ip:
        try:
            ip = requests.get("https://api.ipify.org?format=json", timeout=5).json().get('ip')
        except:
            print("[!] Could not retrieve your IP.")
            input("Press Enter...")
            return
    data = get_geo(ip)
    if data.get('status') == 'fail':
        print(f"[!] Error: {data.get('message')}")
    else:
        print(f"IP: {ip}")
        print(f"Country: {data.get('country')}")
        print(f"Region: {data.get('regionName')}")
        print(f"City: {data.get('city')}")
        print(f"ZIP: {data.get('zip')}")
        print(f"Lat/Lon: {data.get('lat')}, {data.get('lon')}")
        print(f"ISP: {data.get('isp')}")
        print(f"Organization: {data.get('org')}")
        print(f"AS: {data.get('as')}")
        print(f"Timezone: {data.get('timezone')}")
        print(f"Proxy: {'Yes' if data.get('proxy') else 'No'}")
        print(f"Hosting: {'Yes' if data.get('hosting') else 'No'}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()