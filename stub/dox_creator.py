#!/usr/bin/env python3
# SNOOP Dox Creator – génère un dossier d'identité

import os, random, time, requests
from colorama import Fore, Style, init
init(autoreset=True)

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers", "-q"])
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

def token_info(tk):
    h = {"Authorization": tk, "Content-Type": "application/json"}
    try:
        u = requests.get('https://discord.com/api/v9/users/@me', headers=h).json()
        un = f"{u.get('username')}#{u.get('discriminator')}"
        dn = u.get("global_name", "N/A")
        uid = u.get("id", "N/A")
        av = f"https://cdn.discordapp.com/avatars/{uid}/{u.get('avatar')}.png"
        cr = time.ctime(((int(uid) >> 22) + 1420070400000) / 1000)
        em = u.get("email", "N/A")
        ph = u.get("phone", "N/A")
        nit = {0:"False",1:"Nitro Classic",2:"Nitro Boosts",3:"Nitro Basic"}.get(u.get("premium_type"), "False")
        mfa = str(u.get("mfa_enabled", "N/A"))
        return un, dn, uid, av, cr, em, ph, nit, "N/A", "N/A", mfa
    except:
        return ("N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A","N/A")

def phone_info(num):
    try:
        p = phonenumbers.parse(num, None)
        return {
            "Carrier": carrier.name_for_number(p, "en") or "N/A",
            "Type": "Mobile" if phonenumbers.number_type(p) == phonenumbers.PhoneNumberType.MOBILE else "Fixed",
            "Region": phonenumbers.region_code_for_number(p) or "N/A",
            "Location": geocoder.description_for_number(p, "en") or "N/A",
            "Timezone": timezone.time_zones_for_number(p)[0] if timezone.time_zones_for_number(p) else "N/A"
        }
    except:
        return None

def main():
    cl = Fore
    print(f"{cl.MAGENTA}\n  ╔═══════════════════════════════════════╗")
    print(f"  ║         SNOOP DOX CREATOR               ║")
    print(f"  ╚═══════════════════════════════════════╝\n{Style.RESET_ALL}")

    # Nouvel ASCII art SNOOP
    print(f"{cl.CYAN}   _____ _   _  ___  ___  _____ {Style.RESET_ALL}")
    print(f"{cl.CYAN}  / ____| \\ | |/ _ \\| _ \\/ ____|{Style.RESET_ALL}")
    print(f"{cl.CYAN} | (___ |  \\| | | | | |_) | (___ {Style.RESET_ALL}")
    print(f"{cl.CYAN}  \\___ \\| . ` | | | |  _ < \\___ \\{Style.RESET_ALL}")
    print(f"{cl.CYAN}  ____) | |\\  | |_| | |_) |____) |{Style.RESET_ALL}")
    print(f"{cl.CYAN} |_____/|_| \\_|\\___/|____/|_____/ {Style.RESET_ALL}\n")

    fields = {}
    fields["doxed_by"] = input(f"{cl.CYAN}  Doxed by: {Style.RESET_ALL}").strip()
    fields["reason"] = input(f"{cl.CYAN}  Reason: {Style.RESET_ALL}").strip()
    fields["pseudo1"] = input(f"{cl.CYAN}  First pseudo: {Style.RESET_ALL}").strip()
    fields["pseudo2"] = input(f"{cl.CYAN}  Second pseudo: {Style.RESET_ALL}").strip()

    print(f"\n{cl.MAGENTA}  [ DISCORD INFO ]{Style.RESET_ALL}")
    use_token = input(f"{cl.CYAN}  Use token to auto-fill? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
    if use_token:
        tk = input(f"{cl.CYAN}  Token: {Style.RESET_ALL}").strip()
        un, dn, uid, av, cr, em, ph, nit, fr, gc, mfa = token_info(tk)
    else:
        tk = "None"
        un = input("  Username: ").strip()
        dn = input("  Display: ").strip()
        uid = input("  ID: ").strip()
        av = input("  Avatar URL: ").strip()
        cr = input("  Created: ").strip()
        em = input("  Email: ").strip()
        ph = input("  Phone: ").strip()
        nit = input("  Nitro: ").strip()
        fr = input("  Friends: ").strip()
        gc = input("  Gifts: ").strip()
        mfa = input("  MFA: ").strip()

    print(f"\n{cl.MAGENTA}  [ IP INFO ]{Style.RESET_ALL}")
    ip_pub = input(f"{cl.CYAN}  Public IP: {Style.RESET_ALL}").strip()
    ip_loc = input(f"{cl.CYAN}  Local IP: {Style.RESET_ALL}").strip()
    ipv6 = input(f"{cl.CYAN}  IPv6: {Style.RESET_ALL}").strip()
    vpn = input(f"{cl.CYAN}  VPN (y/n): {Style.RESET_ALL}").strip()

    print(f"\n{cl.MAGENTA}  [ PC INFO ]{Style.RESET_ALL}")
    pc_n = input(f"{cl.CYAN}  PC Name: {Style.RESET_ALL}").strip()
    pc_un = input(f"{cl.CYAN}  PC Username: {Style.RESET_ALL}").strip()
    pc_dn = input(f"{cl.CYAN}  PC Display: {Style.RESET_ALL}").strip()
    pc_plt = input(f"{cl.CYAN}  Platform: {Style.RESET_ALL}").strip()
    pc_os = input(f"{cl.CYAN}  OS: {Style.RESET_ALL}").strip()
    pc_key = input(f"{cl.CYAN}  Windows Key: {Style.RESET_ALL}").strip()
    pc_mac = input(f"{cl.CYAN}  MAC: {Style.RESET_ALL}").strip()
    pc_hwid = input(f"{cl.CYAN}  HWID: {Style.RESET_ALL}").strip()
    pc_cpu = input(f"{cl.CYAN}  CPU: {Style.RESET_ALL}").strip()
    pc_gpu = input(f"{cl.CYAN}  GPU: {Style.RESET_ALL}").strip()
    pc_ram = input(f"{cl.CYAN}  RAM: {Style.RESET_ALL}").strip()
    pc_dsk = input(f"{cl.CYAN}  Disk: {Style.RESET_ALL}").strip()

    print(f"\n{cl.MAGENTA}  [ PHONE INFO ]{Style.RESET_ALL}")
    ph_num = input(f"{cl.CYAN}  Phone number (with country code): {Style.RESET_ALL}").strip()
    ph_brd = input(f"{cl.CYAN}  Phone brand: {Style.RESET_ALL}").strip()
    info = phone_info(ph_num)
    if info:
        ph_op = info["Carrier"]
        ph_typ = info["Type"]
        ph_cc = info["Region"]
        ph_reg = info["Location"]
        ph_tz = info["Timezone"]
    else:
        ph_op = ph_typ = ph_cc = ph_reg = ph_tz = "N/A"

    print(f"\n{cl.MAGENTA}  [ PERSONAL INFO ]{Style.RESET_ALL}")
    gender = input(f"{cl.CYAN}  Gender: {Style.RESET_ALL}").strip()
    l_name = input(f"{cl.CYAN}  Last Name: {Style.RESET_ALL}").strip()
    f_name = input(f"{cl.CYAN}  First Name: {Style.RESET_ALL}").strip()
    age = input(f"{cl.CYAN}  Age: {Style.RESET_ALL}").strip()
    mother = input(f"{cl.CYAN}  Mother: {Style.RESET_ALL}").strip()
    father = input(f"{cl.CYAN}  Father: {Style.RESET_ALL}").strip()

    print(f"\n{cl.MAGENTA}  [ LOCATION ]{Style.RESET_ALL}")
    cont = input(f"{cl.CYAN}  Continent: {Style.RESET_ALL}").strip()
    country = input(f"{cl.CYAN}  Country: {Style.RESET_ALL}").strip()
    region = input(f"{cl.CYAN}  Region: {Style.RESET_ALL}").strip()
    zip_c = input(f"{cl.CYAN}  ZIP: {Style.RESET_ALL}").strip()
    city = input(f"{cl.CYAN}  City: {Style.RESET_ALL}").strip()
    addr = input(f"{cl.CYAN}  Address: {Style.RESET_ALL}").strip()

    print(f"\n{cl.MAGENTA}  [ SOCIAL & OTHER ]{Style.RESET_ALL}")
    mail = input(f"{cl.CYAN}  Email: {Style.RESET_ALL}").strip()
    pwd = input(f"{cl.CYAN}  Password: {Style.RESET_ALL}").strip()
    other = input(f"{cl.CYAN}  Other info: {Style.RESET_ALL}").strip()
    db = input(f"{cl.CYAN}  Database leaks: {Style.RESET_ALL}").strip()
    logs = input(f"{cl.CYAN}  Logs: {Style.RESET_ALL}").strip()

    name_file = input(f"{cl.CYAN}  Output filename (no extension): {Style.RESET_ALL}").strip() or f"dox_{random.randint(1,999)}"
    os.makedirs("output/dox", exist_ok=True)
    path = f"output/dox/{name_file}.txt"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"""
    ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                        
            ███████╗███╗   ██╗ ██████╗  ██████╗ ██████╗ 
            ██╔════╝████╗  ██║██╔═══██╗██╔═══██╗██╔══██╗
            ███████╗██╔██╗ ██║██║   ██║██║   ██║██████╔╝
            ╚════██║██║╚██╗██║██║   ██║██║   ██║██╔═══╝ 
            ███████║██║ ╚████║╚██████╔╝╚██████╔╝██║     
            ╚══════╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝     
                              
                                                                                   
            Doxed By : {fields['doxed_by']}
            Reason   : {fields['reason']}
            Pseudo   : "{fields['pseudo1']}", "{fields['pseudo2']}"
    
    ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            DISCORD:
            =====================================================================================
            [+] Username     : {un}
            [+] Display Name : {dn}
            [+] ID           : {uid}
            [+] Avatar       : {av}
            [+] Created At   : {cr}
            [+] Token        : {tk}
            [+] E-Mail       : {em}
            [+] Phone        : {ph}
            [+] Nitro        : {nit}
            [+] Friends      : {fr}
            [+] Gift Code    : {gc}
            [+] MFA          : {mfa}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            INFORMATION:
            =====================================================================================
            +────────────Pc────────────+
            [+] IP Public    : {ip_pub}
            [+] Ip Local     : {ip_loc}
            [+] Ipv6         : {ipv6}
            [+] VPN Y/N      : {vpn}

            [+] Name         : {pc_n}
            [+] Username     : {pc_un}
            [+] Display Name : {pc_dn}

            [+] Plateform    : {pc_plt}
            [+] Exploitation : {pc_os}
            [+] Windows Key  : {pc_key}

            [+] MAC          : {pc_mac}
            [+] HWID         : {pc_hwid}
            [+] CPU          : {pc_cpu}
            [+] GPU          : {pc_gpu}
            [+] RAM          : {pc_ram}
            [+] Disk         : {pc_dsk}

            +───────────Phone──────────+
            [+] Phone Number : {ph_num}
            [+] Brand        : {ph_brd}
            [+] Operator     : {ph_op}
            [+] Type Number  : {ph_typ}
            [+] Country      : {ph_cc}
            [+] Region       : {ph_reg}
            [+] Timezone     : {ph_tz}

            +───────────Personal───────+
            [+] Gender      : {gender}
            [+] Last Name   : {l_name}
            [+] First Name  : {f_name}
            [+] Age         : {age}
            [+] Mother      : {mother}
            [+] Father      : {father}

            +────────────Loc───────────+
            [+] Continent   : {cont}
            [+] Country     : {country}
            [+] Region      : {region}
            [+] Postal Code : {zip_c}
            [+] City        : {city}
            [+] Address     : {addr}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            SOCIAL:
            =====================================================================================
            [+] Email    : {mail}
            [+] Password : {pwd}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            OTHER:
            =====================================================================================
            {other}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            DATABASE:
            =====================================================================================
            {db}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            LOGS:
            =====================================================================================
            {logs}
           ╚═══════════════════════════════════════════════════════════════════════════════════════╝
        """)
    print(f"{Fore.GREEN}  [+] Dox created: {path}{Style.RESET_ALL}")
    input(f"{Fore.CYAN}  Press Enter to return...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()