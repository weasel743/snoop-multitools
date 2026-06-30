#!/usr/bin/env python3
# OSINT: Username Tracker – vérifie la présence sur plusieurs sites

import sys
import requests
import threading
import time

SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Reddit": "https://www.reddit.com/user/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Tumblr": "https://{}.tumblr.com",
    "Spotify": "https://open.spotify.com/user/{}",
    "VK": "https://vk.com/{}",
    "Discord": "https://discord.com/users/{}",  # ne fonctionne pas directement
    "Flickr": "https://www.flickr.com/people/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Dev.to": "https://dev.to/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://twitch.tv/{}",
    "Telegram": "https://t.me/{}",
}

def check_profile(platform, url, username, results):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            results[platform] = True
        else:
            results[platform] = False
    except:
        results[platform] = False

def main():
    print("\n[SNOOP OSINT] Username Tracker")
    username = input("Enter username to search: ").strip()
    if not username:
        print("[!] Username required.")
        input("Press Enter...")
        return
    print(f"\n[+] Searching for '{username}' on {len(SITES)} platforms...")
    results = {}
    threads = []
    for platform, url_template in SITES.items():
        url = url_template.format(username)
        t = threading.Thread(target=check_profile, args=(platform, url, username, results))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    found = []
    for platform, exists in results.items():
        status = "[+] Found" if exists else "[-] Not found"
        print(f"{status}: {platform}")
        if exists:
            found.append(platform)
    print(f"\nTotal found: {len(found)}/{len(SITES)}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()