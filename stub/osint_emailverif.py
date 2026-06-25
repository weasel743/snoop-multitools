#!/usr/bin/env python3
# OSINT: Email Verifier (via vérification syntaxe + domaine MX)

import sys
import re
import dns.resolver

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        return False
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

def main():
    print("\n[SNOOP OSINT] Email Verifier")
    email = input("Enter email address: ").strip()
    if not email:
        print("[!] Email required.")
        input("Press Enter...")
        return
    if is_valid_email(email):
        print("[+] Email is syntactically valid and domain has MX records.")
    else:
        print("[-] Email is invalid or domain has no MX records.")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()