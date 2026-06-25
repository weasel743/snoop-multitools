#!/usr/bin/env python3
# OSINT: Pastebin Dorking (recherche via Google ou alternative)

import sys
import requests

def search_pastebin(query):
    # Utilise une recherche Google personnalisée ou l'API de Pastebin (nécessite clé)
    # Ici on simule une recherche via une requête HTTP vers un site tiers
    try:
        url = f"https://pastebin.com/search?q={query}"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        return r.text
    except Exception as e:
        return str(e)

def main():
    print("\n[SNOOP OSINT] Pastebin Dorking")
    query = input("Enter search keyword: ").strip()
    if not query:
        print("[!] Query required.")
        input("Press Enter...")
        return
    print(f"\n[+] Searching Pastebin for '{query}'...")
    result = search_pastebin(query)
    if len(result) > 100:
        print("Results (first 500 chars):")
        print(result[:500])
    else:
        print("[!] No results or error.")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()