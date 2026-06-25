#!/usr/bin/env python3
# OSINT: Shodan Search (via la recherche publique sans clé)

import sys
import requests
import json

def shodan_search(query):
    # Utilise l'interface publique de Shodan (sans clé) : https://www.shodan.io/search?query=...
    # On va faire une simple requête HTTP pour récupérer les résultats (limités)
    try:
        url = f"https://www.shodan.io/search?query={query}"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            # On extrait les résultats (parsing simplifié)
            return r.text
        else:
            return f"HTTP {r.status_code}"
    except Exception as e:
        return str(e)

def main():
    print("\n[SNOOP OSINT] Shodan Search (public, sans clé)")
    query = input("Enter search query (e.g., 'apache'): ").strip()
    if not query:
        print("[!] Query required.")
        input("Press Enter...")
        return
    print(f"\n[+] Searching Shodan for '{query}'...")
    result = shodan_search(query)
    # Affichage basique des premiers résultats
    if "HTTP" in result or len(result) < 100:
        print(f"[!] Error or no results: {result[:200]}")
    else:
        print("Results (raw HTML, first 500 chars):")
        print(result[:500])
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()