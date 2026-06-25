#!/usr/bin/env python3
# SNOOP Crypto Wallet Scanner – ETH/BNB/BTC/LTC/TRX

import os, sys, time, random, hashlib, hmac, asyncio, aiohttp
from datetime import datetime
from Crypto.Hash import keccak, RIPEMD160
from mnemonic import Mnemonic
from colorama import Fore, Style, init
init(autoreset=True)

# --- BIP32 helpers (simplifiés) ---
class BIP32:
    P = 2**256 - 2**32 - 977
    N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    Gx = 0x79be667ef9dcbbac8f8a95cde78ec21df5e0875c5c7f7f9b7b7b3e7b7b7b7b7b7
    Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    G = (Gx, Gy)

    @classmethod
    def _inv(cls, a, n):
        if a == 0: return 0
        lm, hm = 1, 0
        low, high = a % n, n
        while low > 1:
            r = high // low
            nm, new = hm - r * lm, high - r * low
            lm, low, hm, high = nm, new, lm, low
        return lm % n

    @classmethod
    def _ec_add(cls, p, q):
        if not p: return q
        if not q: return p
        px, py = p; qx, qy = q
        if px == qx and py == qy:
            s = ((3 * px * px) * cls._inv(2 * py, cls.P)) % cls.P
        else:
            if px == qx: return None
            s = ((qy - py) * cls._inv(qx - px, cls.P)) % cls.P
        rx = (s * s - px - qx) % cls.P
        ry = (s * (px - rx) - py) % cls.P
        return (rx, ry)

    @classmethod
    def _ec_mul(cls, k, p):
        res = None; addend = p
        while k:
            if k & 1: res = cls._ec_add(res, addend)
            addend = cls._ec_add(addend, addend)
            k >>= 1
        return res

    @classmethod
    def privkey_to_pubkey(cls, privkey_bytes, compressed=True):
        k = int.from_bytes(privkey_bytes, 'big')
        pt = cls._ec_mul(k, cls.G)
        if pt is None: raise ValueError("Invalid private key")
        x, y = pt
        if compressed:
            prefix = b'\x02' if y % 2 == 0 else b'\x03'
            return prefix + x.to_bytes(32, 'big')
        else:
            return b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

    @classmethod
    def from_seed(cls, seed):
        I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return cls(I[:32], I[32:])

    def __init__(self, private_key, chain_code):
        self.private_key = private_key
        self.chain_code = chain_code

    def child(self, index):
        is_hardened = (index & 0x80000000) != 0
        if is_hardened:
            data = b'\x00' + self.private_key + index.to_bytes(4, 'big')
        else:
            pubkey = self.privkey_to_pubkey(self.private_key, compressed=True)
            data = pubkey + index.to_bytes(4, 'big')
        I = hmac.new(self.chain_code, data, hashlib.sha512).digest()
        Il, Ir = I[:32], I[32:]
        k_par = int.from_bytes(self.private_key, 'big')
        il_int = int.from_bytes(Il, 'big')
        if il_int >= self.N: raise ValueError("Invalid child key")
        child_k = (il_int + k_par) % self.N
        if child_k == 0: raise ValueError("Invalid child key")
        return BIP32(child_k.to_bytes(32, 'big'), Ir)

    def derive_path(self, path):
        parts = path.split('/')
        if parts[0] != 'm': raise ValueError("Path must start with 'm'")
        curr = self
        for part in parts[1:]:
            if part.endswith("'"): index = int(part[:-1]) | 0x80000000
            else: index = int(part)
            curr = curr.child(index)
        return curr

# --- Address generators ---
def base58_encode(b):
    chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(b, 'big')
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(chars[r])
    pad = 0
    for c in b:
        if c == 0: pad += 1
        else: break
    return (chars[0] * pad) + "".join(reversed(res))

def base58_check_encode(version_byte, payload):
    data = version_byte + payload
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return base58_encode(data + checksum)

def ripemd160_hash(data):
    r = RIPEMD160.new(); r.update(data); return r.digest()

def keccak256_hash(data):
    k = keccak.new(digest_bits=256); k.update(data); return k.digest()

def eth_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=False)[1:]
    khash = keccak256_hash(pubkey)
    addr_hex = khash[-20:].hex().lower()
    k = keccak.new(digest_bits=256); k.update(addr_hex.encode('ascii'))
    ahash = k.hexdigest()
    checksum_addr = ""
    for i in range(40):
        if int(ahash[i], 16) >= 8:
            checksum_addr += addr_hex[i].upper()
        else:
            checksum_addr += addr_hex[i]
    return "0x" + checksum_addr

def btc_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=True)
    sha = hashlib.sha256(pubkey).digest()
    pkhash = ripemd160_hash(sha)
    return base58_check_encode(b'\x00', pkhash)

def ltc_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=True)
    sha = hashlib.sha256(pubkey).digest()
    pkhash = ripemd160_hash(sha)
    return base58_check_encode(b'\x30', pkhash)

def trx_address(privkey):
    pubkey = BIP32.privkey_to_pubkey(privkey, compressed=False)[1:]
    khash = keccak256_hash(pubkey)
    pkhash = khash[-20:]
    return base58_check_encode(b'\x41', pkhash)

def generate_wallets(seed_bytes):
    root = BIP32.from_seed(seed_bytes)
    eth_priv = root.derive_path("m/44'/60'/0'/0/0").private_key
    btc_priv = root.derive_path("m/44'/0'/0'/0/0").private_key
    ltc_priv = root.derive_path("m/44'/2'/0'/0/0").private_key
    trx_priv = root.derive_path("m/44'/195'/0'/0/0").private_key
    return (
        eth_address(eth_priv),
        btc_address(btc_priv),
        ltc_address(ltc_priv),
        trx_address(trx_priv),
    )

async def get_balance(session, address, network):
    timeout = aiohttp.ClientTimeout(total=10)
    if network == "btc":
        url = f"https://blockstream.info/api/address/{address}"
        try:
            async with session.get(url, timeout=timeout) as r:
                if r.status == 200:
                    d = await r.json()
                    chain = d.get("chain_stats", {})
                    return str(chain.get("funded_txo_sum", 0) - chain.get("spent_txo_sum", 0))
                if r.status == 429:
                    await asyncio.sleep(2)
                    return await get_balance(session, address, network)
        except: pass
        return "0"
    if network == "trx":
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        try:
            async with session.get(url, timeout=timeout) as r:
                if r.status == 200:
                    data = (await r.json()).get("data", [])
                    return str(data[0].get("balance", 0)) if data else "0"
        except: pass
        return "0"
    endpoints = {
        "eth": f"https://ethbook.guarda.co/api/v2/address/{address}",
        "bnb": f"https://bsc-nn.atomicwallet.io/api/v2/address/{address}",
        "ltc": f"https://litecoin.atomicwallet.io/api/v2/address/{address}",
    }
    try:
        async with session.get(endpoints[network], timeout=timeout) as r:
            if r.status == 200:
                return str((await r.json()).get("balance", "0"))
            if r.status == 429:
                await asyncio.sleep(2)
                return await get_balance(session, address, network)
    except: pass
    return "0"

def save_wallet(network, address, balance, mnemonic, priv_key):
    os.makedirs("found_wallets", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"found_wallets/{network}_{ts}.txt"
    with open(filename, "w") as f:
        f.write(f"Network      : {network}\n")
        f.write(f"Address      : {address}\n")
        f.write(f"Balance      : {balance}\n\n")
        f.write(f"Mnemonic     : {mnemonic}\n")
        f.write(f"Private Key  : {priv_key}\n")
    return filename

async def worker(session, word_count, stats, print_lock):
    mnemo = Mnemonic("english")
    while True:
        mnemonic_str = mnemo.generate(strength=128 if word_count == 12 else 256)
        seed_bytes = mnemo.to_seed(mnemonic_str, passphrase="")
        eth_addr, btc_addr, ltc_addr, trx_addr = generate_wallets(seed_bytes)
        results = await asyncio.gather(
            get_balance(session, eth_addr, "eth"),
            get_balance(session, eth_addr, "bnb"),
            get_balance(session, btc_addr, "btc"),
            get_balance(session, ltc_addr, "ltc"),
            get_balance(session, trx_addr, "trx"),
            return_exceptions=True
        )
        stats["generated"] += 1
        def val(raw, dec):
            return 0.0 if isinstance(raw, Exception) else int(raw) / 10**dec
        e_val = val(results[0], 18)
        b_val = val(results[1], 18)
        btc_val = val(results[2], 8)
        ltc_val = val(results[3], 8)
        trx_val = val(results[4], 6)
        found = any(v > 0 for v in [e_val, b_val, btc_val, ltc_val, trx_val])
        if found:
            stats["found"] += 1
            fp = ""
            if e_val > 0: fp = save_wallet("ETH", eth_addr, e_val, mnemonic_str, seed_bytes.hex())
            if b_val > 0: fp = save_wallet("BNB", eth_addr, b_val, mnemonic_str, seed_bytes.hex())
            if btc_val > 0: fp = save_wallet("BTC", btc_addr, btc_val, mnemonic_str, seed_bytes.hex())
            if ltc_val > 0: fp = save_wallet("LTC", ltc_addr, ltc_val, mnemonic_str, seed_bytes.hex())
            if trx_val > 0: fp = save_wallet("TRX", trx_addr, trx_val, mnemonic_str, seed_bytes.hex())
            async with print_lock:
                print(f"\n{Fore.MAGENTA}  {'█'*68}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}  [$$$]  WALLET WITH BALANCE FOUND  [$$$]{Style.RESET_ALL}")
                print(f"{Fore.CYAN}  {'─'*68}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  SEED    : {Style.RESET_ALL}{mnemonic_str}")
                print(f"{Fore.YELLOW}  ETH/BNB : {Style.RESET_ALL}{eth_addr}  →  ETH:{e_val}  BNB:{b_val}")
                print(f"{Fore.YELLOW}  BTC     : {Style.RESET_ALL}{btc_addr}  →  {btc_val}")
                print(f"{Fore.YELLOW}  LTC     : {Style.RESET_ALL}{ltc_addr}  →  {ltc_val}")
                print(f"{Fore.YELLOW}  TRX     : {Style.RESET_ALL}{trx_addr}  →  {trx_val}")
                print(f"{Fore.CYAN}  Saved   : {fp}{Style.RESET_ALL}")
                print(f"{Fore.MAGENTA}  {'█'*68}\n{Style.RESET_ALL}")
        # Print progress line (shortened)
        seed_s = mnemonic_str[:12] + ".."
        e_s = f"{eth_addr[:5]}..{eth_addr[-3:]}"
        btc_s = f"{btc_addr[:5]}..{btc_addr[-3:]}"
        ltc_s = f"{ltc_addr[:5]}..{ltc_addr[-3:]}"
        trx_s = f"{trx_addr[:5]}..{trx_addr[-3:]}"
        bal = f"{Fore.GREEN}E:{e_val} B:{b_val} BTC:{btc_val} LTC:{ltc_val} TRX:{trx_val}{Style.RESET_ALL}" if found else "0"
        async with print_lock:
            print(f"SEED:{Fore.MAGENTA}{seed_s:<14}{Style.RESET_ALL} | E/B:{Fore.CYAN}{e_s}{Style.RESET_ALL} BTC:{Fore.YELLOW}{btc_s}{Style.RESET_ALL} LTC:{Fore.CYAN}{ltc_s}{Style.RESET_ALL} TRX:{Fore.RED}{trx_s}{Style.RESET_ALL} | BAL:{bal}")

async def main_async(num_workers, word_count):
    stats = {"generated": 0, "found": 0}
    print_lock = asyncio.Lock()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}  {'═'*50}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  {'':^4}Crypto Wallet Scanner  v3.0{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  {'':^4}ETH  /  BNB  /  BTC  /  LTC  /  TRX{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  {'═'*50}\n{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  Workers : {num_workers}   |   Seed Words : {word_count}{Style.RESET_ALL}\n")
    connector = aiohttp.TCPConnector(limit=500, limit_per_host=100, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session, word_count, stats, print_lock)) for _ in range(num_workers)]
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            pass

def main():
    print(f"{Fore.MAGENTA}\n  ╔══════════════════════════════════════════╗")
    print(f"  ║       ETH  BNB  BTC  LTC  TRX            ║")
    print(f"  ╚══════════════════════════════════════════╝\n{Style.RESET_ALL}")
    try:
        w = input(f"{Fore.CYAN}  Workers (default 50): {Style.RESET_ALL}").strip()
        num_workers = int(w) if w else 50
    except:
        num_workers = 50
    print(f"{Fore.CYAN}  Choose seed words: 12 or 24 (default 12): {Style.RESET_ALL}")
    wc = input().strip()
    word_count = 12 if wc not in ["12","24"] else int(wc)
    print(f"{Fore.GREEN}  [*] Starting {num_workers} workers with {word_count}-word seeds...{Style.RESET_ALL}\n")
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main_async(num_workers, word_count))
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}  [!] Scanner stopped by user.{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()