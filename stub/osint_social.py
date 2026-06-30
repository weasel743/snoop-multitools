import sys
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    "Pinterest": "https://www.pinterest.com/{}/",
    "Tumblr": "https://{}.tumblr.com",
    "Spotify": "https://open.spotify.com/user/{}",
    "VK": "https://vk.com/{}",
    "Flickr": "https://www.flickr.com/people/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Dev.to": "https://dev.to/{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Twitch": "https://twitch.tv/{}",
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

def check_profile(platform, url, username):
    try:
        headers = {"User-Agent": USER_AGENTS[hash(username + platform) % len(USER_AGENTS)]}
        r = requests.get(url, timeout=5, headers=headers)
        if r.status_code == 200:
            return platform, True
        else:
            return platform, False
    except:
        return platform, False

def main():
    print("\n[SNOOP OSINT] Social Media Profile Scraper")
    username = input("Enter username: ").strip()
    if not username:
        print("[!] Username required.")
        input("Press Enter...")
        return
    print(f"\n[+] Checking presence of '{username}' on social media...")
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for platform, url_template in SITES_SOCIAL.items():
            url = url_template.format(username)
            futures[executor.submit(check_profile, platform, url, username)] = platform
        for future in as_completed(futures):
            platform, exists = future.result()
            results[platform] = exists
    found = []
    for platform, exists in results.items():
        status = "[+] Found" if exists else "[-] Not found"
        print(f"{status}: {platform}")
        if exists:
            found.append(platform)
    print(f"\nTotal found: {len(found)}/{len(SITES_SOCIAL)}")
    if found:
        print("Found on: " + ", ".join(found))
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()