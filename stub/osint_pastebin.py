import sys
import re
import requests
import urllib.parse

def search_google(query):
    try:
        encoded = urllib.parse.quote(f'site:pastebin.com {query}')
        url = f"https://www.google.com/search?q={encoded}&num=10"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
        r = requests.get(url, timeout=10, headers=headers)
        if r.status_code == 200:
            results = []
            for match in re.finditer(r'<a[^>]+href="(https://pastebin\.com/[^"]+)"[^>]*>([^<]+)</a>', r.text, re.I):
                url = match.group(1)
                title = match.group(2).strip()
                if "pastebin.com" in url:
                    results.append((url, title))
            return results
        return []
    except Exception as e:
        return []

def search_pastebin_direct(query):
    try:
        url = f"https://pastebin.com/search?q={query}"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            results = []
            for match in re.finditer(r'href="(https://pastebin\.com/[^"]+)"', r.text, re.I):
                results.append(match.group(1))
            return results[:20]
        return []
    except:
        return []

def main():
    print("\n[SNOOP OSINT] Pastebin Dorking")
    query = input("Enter search keyword: ").strip()
    if not query:
        print("[!] Query required.")
        input("Press Enter...")
        return
    print(f"\n[+] Searching for '{query}'...")
    print("[*] Searching via Google (site:pastebin.com)...")
    google_results = search_google(query)
    if google_results:
        print(f"[+] Found {len(google_results)} results via Google:")
        for i, (url, title) in enumerate(google_results[:10], 1):
            print(f"  {i}. {title[:50]}")
            print(f"     {url}")
    else:
        print("[!] No results via Google.")
    print("\n[*] Trying direct Pastebin search...")
    direct_results = search_pastebin_direct(query)
    if direct_results:
        print(f"[+] Found {len(direct_results)} results directly:")
        for i, url in enumerate(direct_results[:10], 1):
            print(f"  {i}. {url}")
    else:
        print("[!] No direct results.")
    if not google_results and not direct_results:
        print("\n[!] No results found. Try a different keyword.")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()