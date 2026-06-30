#!/usr/bin/env python3
# SNOOP Selfbot – Advanced Discord Selfbot
# SNOOP – Advanced Toolkit

import json, os, re, random, threading, time, sys
import requests, websocket
from datetime import datetime
from colorama import Fore, Style

# --- Configuration ---
LOGDIR = "logs"
CFG_FILE = "snoop_config.json"  # utilisé pour stocker les paramètres du selfbot
os.makedirs(LOGDIR, exist_ok=True)

class SnoopSelfbot:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.running = False
        self.user_id = None
        self.username = None

        self.nitro_sniper = False
        self.auto_responder = False
        self.triggers = {}
        self.logger = False
        self.dm_logger = False
        self.ghost_mode = False
        self.ghost_delay = 5
        self.status_rotator = False
        self.statuses = []
        self.anti_spam = False
        self.reaction_adder = False
        self.reaction_emoji = "✅"
        self.reaction_channel = None
        self.typing_loop = False
        self.typing_channel = None

        self.ws = None
        self.heartbeat_interval = None
        self.seen_messages = set()
        self._stop_event = threading.Event()
        self._session_id = None
        self._last_seq = None
        self._reconnect = False

    def log(self, msg, level="ok"):
        icons = {"ok": "+", "warn": "~", "err": "!", "info": "*"}
        colors = {"ok": Fore.MAGENTA, "warn": Fore.YELLOW, "err": Fore.RED, "info": Fore.CYAN}
        sym = icons.get(level, "+")
        col = colors.get(level, Fore.WHITE)
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"{col}  [{sym}] {ts}  {msg}{Style.RESET_ALL}")

    def _flog(self, cat, line):
        p = os.path.join(LOGDIR, f"selfbot_{cat}.log")
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {line}\n")

    def save_settings(self):
        payload = {
            "nitro_sniper": self.nitro_sniper,
            "auto_responder": self.auto_responder,
            "triggers": self.triggers,
            "logger": self.logger,
            "dm_logger": self.dm_logger,
            "ghost_mode": self.ghost_mode,
            "ghost_delay": self.ghost_delay,
            "status_rotator": self.status_rotator,
            "statuses": self.statuses,
            "anti_spam": self.anti_spam,
            "reaction_adder": self.reaction_adder,
            "reaction_emoji": self.reaction_emoji,
            "reaction_channel": self.reaction_channel,
            "typing_loop": False,
            "typing_channel": self.typing_channel,
        }
        try:
            # Charger la config existante pour ne pas écraser les autres clés
            cfg = {}
            if os.path.exists(CFG_FILE):
                with open(CFG_FILE, 'r') as f:
                    cfg = json.load(f)
            cfg["selfbot"] = payload
            with open(CFG_FILE, 'w') as f:
                json.dump(cfg, f, indent=2)
        except Exception as e:
            self.log(f"save failed: {e}", "err")

    def load_settings(self):
        try:
            if not os.path.exists(CFG_FILE):
                return
            with open(CFG_FILE, 'r') as f:
                cfg = json.load(f)
            sb = cfg.get("selfbot", {})
            for k, default in [
                ("nitro_sniper", False), ("auto_responder", False),
                ("triggers", {}), ("logger", False), ("dm_logger", False),
                ("ghost_mode", False), ("ghost_delay", 5),
                ("status_rotator", False), ("statuses", []),
                ("anti_spam", False), ("reaction_adder", False),
                ("reaction_emoji", "✅"), ("reaction_channel", None),
                ("typing_channel", None),
            ]:
                setattr(self, k, sb.get(k, default))
            self.log("settings loaded", "info")
        except Exception as e:
            self.log(f"load failed: {e}", "warn")

    # ---- Requêtes HTTP ----
    def _req(self, method, endpoint, **kw):
        url = f"https://discord.com/api/v9{endpoint}"
        try:
            return getattr(requests, method)(url, headers=self.headers, timeout=10, **kw)
        except Exception as e:
            self.log(f"{method.upper()} {endpoint}: {e}", "err")
            return None

    def _get(self, ep): return self._req("get", ep)
    def _post(self, ep, j=None): return self._req("post", ep, json=j)
    def _delete(self, ep): return self._req("delete", ep)
    def _patch(self, ep, j=None): return self._req("patch", ep, json=j)

    def fetch_user(self):
        r = self._get("/users/@me")
        if r and r.status_code == 200:
            d = r.json()
            self.user_id = d["id"]
            disc = d.get("discriminator", "0")
            self.username = d["username"] + (f"#{disc}" if disc not in ("0", None) else "")
            return True
        return False

    # ---- WebSocket gestion ----
    def on_message(self, ws, raw):
        try:
            data = json.loads(raw)
        except:
            return
        op = data.get("op")
        t = data.get("t")
        d = data.get("d") or {}
        s = data.get("s")
        if s is not None:
            self._last_seq = s
        if op == 10:
            self.heartbeat_interval = d["heartbeat_interval"] / 1000
            threading.Thread(target=self.heartbeat, args=(ws,), daemon=True).start()
            if self._reconnect and self._session_id:
                self._resume(ws)
            else:
                self.identify(ws)
        elif op == 7:
            self._reconnect = True
            try: ws.close()
            except: pass
        elif op == 9:
            self._reconnect = False
            self._session_id = None
            self._last_seq = None
            time.sleep(random.uniform(1, 5))
            self.identify(ws)

        if t == "READY":
            self._session_id = d.get("session_id")
            self._reconnect = False
            self.running = True
            self.log(f"ready -> {self.username}")
        if t == "RESUMED":
            self.running = True
            self.log("session resumed", "info")
        if t == "MESSAGE_CREATE":
            self._handle_msg(d)
        if t == "MESSAGE_DELETE" and self.logger:
            self.log(f"del ch:{d.get('channel_id')} id:{d.get('id')}", "warn")
        if t == "MESSAGE_UPDATE" and self.logger:
            self.log(f"edit ch:{d.get('channel_id')} -> {d.get('content','')[:80]}", "warn")

    def heartbeat(self, ws):
        while self.running and not self._stop_event.is_set():
            try:
                ws.send(json.dumps({"op": 1, "d": self._last_seq}))
            except:
                break
            time.sleep(self.heartbeat_interval)

    def identify(self, ws):
        try:
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "properties": {"$os": "windows", "$browser": "chrome", "$device": "pc"},
                    "presence": {"status": "online", "activities": [], "since": None, "afk": False}
                }
            }))
        except Exception as e:
            self.log(f"identify err: {e}", "err")

    def _resume(self, ws):
        try:
            ws.send(json.dumps({
                "op": 6,
                "d": {"token": self.token, "session_id": self._session_id, "seq": self._last_seq}
            }))
        except Exception as e:
            self.log(f"resume err: {e}", "err")

    def _handle_msg(self, d):
        content = d.get("content", "")
        author = d.get("author") or {}
        author_id = author.get("id")
        channel_id = d.get("channel_id")
        msg_id = d.get("id")
        is_dm = d.get("guild_id") is None

        if self.anti_spam:
            k = f"{channel_id}:{content}"
            if k in self.seen_messages:
                return
            self.seen_messages.add(k)
            if len(self.seen_messages) > 500:
                self.seen_messages.clear()

        if self.nitro_sniper and "discord.gift/" in content:
            m = re.search(r"discord\.gift/(\w+)", content)
            if m:
                threading.Thread(target=self._snipe, args=(m.group(1),), daemon=True).start()

        if self.auto_responder and author_id != self.user_id:
            for trig, resp in self.triggers.items():
                if trig.lower() in content.lower():
                    self.send_msg(channel_id, resp)
                    break

        if self.ghost_mode and author_id == self.user_id:
            threading.Thread(target=self._del_after, args=(channel_id, msg_id, self.ghost_delay), daemon=True).start()

        if self.reaction_adder:
            if self.reaction_channel is None or self.reaction_channel == channel_id:
                threading.Thread(target=self._react, args=(channel_id, msg_id, self.reaction_emoji), daemon=True).start()

        if self.dm_logger and is_dm and author_id != self.user_id:
            uname = f"{author.get('username','?')}#{author.get('discriminator','0')}"
            self._flog("dms", f"{uname} ({author_id}) ch:{channel_id} | {content}")
            self.log(f"DM from {uname}: {content[:60]}", "info")

    def _snipe(self, code):
        self.log(f"sniping {code}", "info")
        r = self._post(f"/entitlements/gift-codes/{code}/redeem")
        if r and r.status_code == 200:
            self.log(f"claimed! {code}")
        else:
            self.log(f"snipe failed: {r.json() if r else 'no resp'}", "err")

    def send_msg(self, channel_id, content):
        self._post(f"/channels/{channel_id}/messages", {"content": content})

    def _del_after(self, channel_id, msg_id, delay):
        time.sleep(delay)
        self._delete(f"/channels/{channel_id}/messages/{msg_id}")

    def _react(self, channel_id, msg_id, emoji):
        try:
            import urllib.parse
            e = urllib.parse.quote(emoji)
            requests.put(
                f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg_id}/reactions/{e}/@me",
                headers=self.headers, timeout=5
            )
        except:
            pass

    def rotate_status(self):
        while self.status_rotator and self.running:
            for s in self.statuses:
                if not self.status_rotator or not self.running:
                    return
                self._patch("/users/@me/settings", {"custom_status": {"text": s.strip()}})
                time.sleep(10)

    def set_presence(self, status="online", name="", atype=0, emoji=None):
        acts = []
        if name:
            a = {"type": atype, "name": name}
            if emoji:
                a["emoji"] = {"name": emoji}
            acts.append(a)
        if self.ws:
            try:
                self.ws.send(json.dumps({
                    "op": 3,
                    "d": {"since": None, "activities": acts, "status": status, "afk": False}
                }))
                self.log(f"presence -> [{status}] {name}")
            except Exception as e:
                self.log(f"presence err: {e}", "err")

    def typing_loop_fn(self, channel_id):
        while self.typing_loop and self.running:
            self._post(f"/channels/{channel_id}/typing")
            time.sleep(8)

    def mass_dm(self, msg):
        r = self._get("/users/@me/relationships")
        if not r or r.status_code != 200:
            self.log("cant fetch friends", "err")
            return
        sent = 0
        for f in r.json():
            if f.get("type") != 1:
                continue
            uid = f.get("id") or f.get("user", {}).get("id")
            cr = self._post("/users/@me/channels", {"recipient_id": uid})
            if cr and cr.status_code == 200:
                self.send_msg(cr.json()["id"], msg)
                sent += 1
                self.log(f"sent -> {f.get('user',{}).get('username', uid)}")
                time.sleep(1.5)
        self.log(f"done, sent to {sent} friends")

    def spam_channel(self, channel_id, message, amount, delay=0.8):
        for i in range(amount):
            self.send_msg(channel_id, message)
            self.log(f"[{i+1}/{amount}]", "info")
            time.sleep(delay)
        self.log("spam done")

    def purge_own(self, channel_id, limit=50):
        r = self._get(f"/channels/{channel_id}/messages?limit=100")
        if not r or r.status_code != 200:
            self.log("fetch failed", "err")
            return
        gone = 0
        for m in r.json():
            if m.get("author", {}).get("id") != self.user_id:
                continue
            res = self._delete(f"/channels/{channel_id}/messages/{m['id']}")
            if res and res.status_code == 204:
                gone += 1
            time.sleep(0.5)
            if gone >= limit:
                break
        self.log(f"purged {gone}")

    def nuke_guild(self, guild_id, mode="channels"):
        self.log(f"nuking {guild_id} mode={mode}", "warn")
        targets = []
        if mode in ("channels", "all"):
            r = self._get(f"/guilds/{guild_id}/channels")
            if r and r.status_code == 200:
                targets = [("/channels/" + c["id"], c.get("name")) for c in r.json()]
        for ep, name in targets:
            res = self._delete(ep)
            ok = res and res.status_code in (200, 204)
            self.log(f"  {'ok' if ok else 'fail'} {name}", "info" if ok else "err")
            time.sleep(0.3)
        if mode in ("roles", "all"):
            r = self._get(f"/guilds/{guild_id}/roles")
            if r and r.status_code == 200:
                for role in r.json():
                    if role["name"] == "@everyone":
                        continue
                    self._delete(f"/guilds/{guild_id}/roles/{role['id']}")
                    time.sleep(0.3)
        self.log("nuke done")

    def fr_spam(self, uids):
        for uid in uids:
            r = self._post(f"/users/@me/relationships/{uid.strip()}", {})
            ok = r and r.status_code in (200, 204)
            self.log(f"fr {uid}: {'ok' if ok else 'fail'}", "info")
            time.sleep(1)

    def join_server(self, code):
        code = code.strip().split("/")[-1]
        r = self._post(f"/invites/{code}")
        if r and r.status_code == 200:
            self.log(f"joined: {r.json().get('guild',{}).get('name','?')}")
        else:
            self.log(f"join fail: {r.text if r else '?'}", "err")

    def _ws_once(self):
        self.ws = websocket.WebSocketApp(
            "wss://gateway.discord.gg/?v=9&encoding=json",
            on_message=self.on_message,
            on_error=lambda ws, e: self.log(f"ws err: {e}", "err"),
            on_close=lambda ws, *a: None,
        )
        self.ws.run_forever(ping_interval=30, ping_timeout=10)

    def _loop(self):
        wait = 1
        while not self._stop_event.is_set():
            self.running = False
            try:
                self._ws_once()
            except Exception as e:
                self.log(f"ws exception: {e}", "err")
            if self._stop_event.is_set():
                break
            self.log(f"disconnected, retry in {wait}s", "warn")
            self._reconnect = True
            time.sleep(wait)
            wait = min(wait * 2, 60)

    def start(self):
        self._stop_event.clear()
        threading.Thread(target=self._loop, daemon=True).start()
        for _ in range(100):
            if self.running:
                break
            time.sleep(0.1)

    def stop(self):
        self._stop_event.set()
        self.running = False
        try:
            if self.ws:
                self.ws.close()
        except:
            pass

# ---- Menu interactif ----
def draw_menu(bot):
    print(f"\n{Fore.MAGENTA}  [ SELFBOT  ─  {bot.username} ]{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}  TOGGLES{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ────────────────────────────────────────{Style.RESET_ALL}")
    # Affichage des toggles
    toggles = [
        ("1", "Nitro Sniper", bot.nitro_sniper),
        ("2", "Auto Responder", bot.auto_responder),
        ("3", "Edit/Del Logger", bot.logger),
        ("4", "Ghost Mode", bot.ghost_mode),
        ("5", "Status Rotator", bot.status_rotator),
        ("6", "Anti Spam", bot.anti_spam),
        ("7", "Auto Reactor", bot.reaction_adder),
        ("8", "Typing Loop", bot.typing_loop),
        ("9", "DM Logger", bot.dm_logger),
    ]
    for k, lbl, flag in toggles:
        state = f"{Fore.GREEN}[ON]{Style.RESET_ALL}" if flag else f"{Fore.RED}[OFF]{Style.RESET_ALL}"
        print(f"  {Fore.YELLOW}[{k}]{Style.RESET_ALL} {lbl:<20} {state}")

    print(f"\n{Fore.CYAN}  CONFIG{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}[10]{Style.RESET_ALL} Setup Triggers    {Fore.YELLOW}[11]{Style.RESET_ALL} Setup Statuses")
    print(f"  {Fore.YELLOW}[12]{Style.RESET_ALL} Set Presence")
    print(f"\n{Fore.CYAN}  ACTIONS{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}[20]{Style.RESET_ALL} Mass DM Friends    {Fore.YELLOW}[21]{Style.RESET_ALL} Channel Spammer")
    print(f"  {Fore.YELLOW}[22]{Style.RESET_ALL} Purge Own Msgs     {Fore.YELLOW}[23]{Style.RESET_ALL} Server Nuke")
    print(f"  {Fore.YELLOW}[24]{Style.RESET_ALL} Friend Spammer     {Fore.YELLOW}[25]{Style.RESET_ALL} Join Server")
    print(f"\n  {Fore.YELLOW}[99]{Style.RESET_ALL} Terminate & Exit")
    print()

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║   SNOOP SELFBOT – Advanced Mode    ║")
    print(f"  ╚═══════════════════════════════════════╝{Style.RESET_ALL}")
    token = input(f"{Fore.CYAN}  Token: {Style.RESET_ALL}").strip()
    if not token:
        print(f"{Fore.RED}  [!] Token required.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    bot = SnoopSelfbot(token)
    if not bot.fetch_user():
        print(f"{Fore.RED}  [!] Invalid Token.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    bot.load_settings()
    bot.start()

    while True:
        draw_menu(bot)
        c = input(f"{Fore.MAGENTA}  snoop@selfbot:~# {Style.RESET_ALL}").strip()
        if c == "1":
            bot.nitro_sniper = not bot.nitro_sniper
            bot.log(f"nitro sniper {'on' if bot.nitro_sniper else 'off'}")
            bot.save_settings()
        elif c == "2":
            bot.auto_responder = not bot.auto_responder
            bot.log(f"auto responder {'on' if bot.auto_responder else 'off'}")
            bot.save_settings()
        elif c == "3":
            bot.logger = not bot.logger
            bot.log(f"logger {'on' if bot.logger else 'off'}")
            bot.save_settings()
        elif c == "4":
            bot.ghost_mode = not bot.ghost_mode
            if bot.ghost_mode:
                try:
                    bot.ghost_delay = int(input(f"{Fore.CYAN}  delay (sec): {Style.RESET_ALL}") or 5)
                except:
                    bot.ghost_delay = 5
            bot.log(f"ghost mode {'on' if bot.ghost_mode else 'off'}")
            bot.save_settings()
        elif c == "5":
            bot.status_rotator = not bot.status_rotator
            if bot.status_rotator and bot.statuses:
                threading.Thread(target=bot.rotate_status, daemon=True).start()
            bot.log(f"status rotator {'on' if bot.status_rotator else 'off'}")
            bot.save_settings()
        elif c == "6":
            bot.anti_spam = not bot.anti_spam
            bot.log(f"anti spam {'on' if bot.anti_spam else 'off'}")
            bot.save_settings()
        elif c == "7":
            bot.reaction_adder = not bot.reaction_adder
            if bot.reaction_adder:
                bot.reaction_emoji = input(f"{Fore.CYAN}  emoji (default ✅): {Style.RESET_ALL}") or "✅"
                bot.reaction_channel = input(f"{Fore.CYAN}  channel id (blank=all): {Style.RESET_ALL}").strip() or None
            bot.log(f"auto reactor {'on' if bot.reaction_adder else 'off'}")
            bot.save_settings()
        elif c == "8":
            bot.typing_loop = not bot.typing_loop
            if bot.typing_loop:
                bot.typing_channel = input(f"{Fore.CYAN}  channel id: {Style.RESET_ALL}").strip()
                threading.Thread(target=bot.typing_loop_fn, args=(bot.typing_channel,), daemon=True).start()
            bot.log(f"typing loop {'on' if bot.typing_loop else 'off'}")
            bot.save_settings()
        elif c == "9":
            bot.dm_logger = not bot.dm_logger
            bot.log(f"dm logger {'on' if bot.dm_logger else 'off'}")
            bot.save_settings()
        elif c == "10":
            bot.log("format: word:reply,word2:reply2")
            t = input(f"{Fore.CYAN}  triggers: {Style.RESET_ALL}")
            try:
                n = 0
                for pair in t.split(","):
                    if ":" not in pair:
                        continue
                    k, v = pair.split(":", 1)
                    bot.triggers[k.strip()] = v.strip()
                    n += 1
                bot.log(f"set {n} triggers ({len(bot.triggers)} total)")
                bot.save_settings()
            except Exception as e:
                bot.log(str(e), "err")
            time.sleep(1)
        elif c == "11":
            raw = input(f"{Fore.CYAN}  statuses (comma sep): {Style.RESET_ALL}")
            bot.statuses = [x.strip() for x in raw.split(",") if x.strip()]
            bot.log(f"set {len(bot.statuses)} statuses")
            bot.save_settings()
            time.sleep(1)
        elif c == "12":
            print(f"{Fore.CYAN}  online | idle | dnd | invisible{Style.RESET_ALL}")
            st = input(f"{Fore.CYAN}  status: {Style.RESET_ALL}") or "online"
            nm = input(f"{Fore.CYAN}  activity name: {Style.RESET_ALL}")
            try:
                at = int(input(f"{Fore.CYAN}  type 0=play 1=stream 2=listen 3=watch: {Style.RESET_ALL}") or 0)
            except:
                at = 0
            em = input(f"{Fore.CYAN}  emoji: {Style.RESET_ALL}") or None
            bot.set_presence(st, nm, at, em)
            time.sleep(1)
        elif c == "20":
            msg = input(f"{Fore.CYAN}  message: {Style.RESET_ALL}")
            threading.Thread(target=bot.mass_dm, args=(msg,), daemon=True).start()
            input(f"{Fore.CYAN}  [running in bg, enter to return]{Style.RESET_ALL}")
        elif c == "21":
            ch = input(f"{Fore.CYAN}  channel id: {Style.RESET_ALL}")
            msg = input(f"{Fore.CYAN}  message: {Style.RESET_ALL}")
            try:
                amt = int(input(f"{Fore.CYAN}  amount: {Style.RESET_ALL}") or 10)
            except:
                amt = 10
            try:
                dl = float(input(f"{Fore.CYAN}  delay (s): {Style.RESET_ALL}") or 0.8)
            except:
                dl = 0.8
            threading.Thread(target=bot.spam_channel, args=(ch.strip(), msg, amt, dl), daemon=True).start()
            input(f"{Fore.CYAN}  [running in bg, enter to return]{Style.RESET_ALL}")
        elif c == "22":
            ch = input(f"{Fore.CYAN}  channel id: {Style.RESET_ALL}")
            try:
                lim = int(input(f"{Fore.CYAN}  max delete: {Style.RESET_ALL}") or 50)
            except:
                lim = 50
            threading.Thread(target=bot.purge_own, args=(ch.strip(), lim), daemon=True).start()
            input(f"{Fore.CYAN}  [running in bg, enter to return]{Style.RESET_ALL}")
        elif c == "23":
            print(f"{Fore.RED}  [!] irreversible!{Style.RESET_ALL}")
            gid = input(f"{Fore.CYAN}  guild id: {Style.RESET_ALL}")
            mode = input(f"{Fore.CYAN}  mode (channels/roles/all): {Style.RESET_ALL}") or "channels"
            if input(f"{Fore.RED}  type NUKE: {Style.RESET_ALL}") == "NUKE":
                threading.Thread(target=bot.nuke_guild, args=(gid.strip(), mode), daemon=True).start()
                input(f"{Fore.CYAN}  [running, enter to return]{Style.RESET_ALL}")
            else:
                bot.log("cancelled", "warn")
                time.sleep(1)
        elif c == "24":
            raw = input(f"{Fore.CYAN}  user ids (comma sep): {Style.RESET_ALL}")
            uids = [x.strip() for x in raw.split(",") if x.strip()]
            threading.Thread(target=bot.fr_spam, args=(uids,), daemon=True).start()
            input(f"{Fore.CYAN}  [running in bg, enter to return]{Style.RESET_ALL}")
        elif c == "25":
            inv = input(f"{Fore.CYAN}  invite: {Style.RESET_ALL}")
            bot.join_server(inv)
            time.sleep(1)
        elif c == "99":
            bot.stop()
            break

if __name__ == "__main__":
    main()