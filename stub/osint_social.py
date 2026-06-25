#!/usr/bin/env python3
# OSINT: Social Media Profile Scraper (vérifie présence sur les réseaux)

import sys
import requests

SITES_SOCIAL = {
    "Facebook": "https://www.facebook.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Twitter": "https://twitter.com/{}",
    "YouTube": "https://www.youtube.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Telegram": "https://t.me/{}",
    "GitHub": "https://github.com/{}",
}

def check_profile(platform, url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def main():
    print("\n[SNOOP OSINT] Social Media Profile Scraper")
    username = input("Enter username: ").strip()
    if not username:
        print("[!] Username required.")
        input("Press Enter...")
        return
    print(f"\n[+] Checking presence of '{username}' on social media...")
    for platform, url_template in SITES_SOCIAL.items():
        url = url_template.format(username)
        exists = check_profile(platform, url)
        status = "[+] Found" if exists else "[-] Not found"
        print(f"{status}: {platform}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()