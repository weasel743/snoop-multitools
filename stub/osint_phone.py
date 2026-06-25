#!/usr/bin/env python3
# OSINT: Phone Number Lookup (utilise phonenumbers, sans clé)

import sys
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def lookup(phone_str):
    try:
        number = phonenumbers.parse(phone_str, None)
        if not phonenumbers.is_valid_number(number):
            return {"valid": False, "error": "Invalid number"}
        info = {
            "valid": True,
            "country": geocoder.description_for_number(number, "en"),
            "carrier": carrier.name_for_number(number, "en"),
            "timezone": timezone.time_zones_for_number(number)
        }
        return info
    except Exception as e:
        return {"valid": False, "error": str(e)}

def main():
    print("\n[SNOOP OSINT] Phone Number Lookup")
    phone = input("Enter phone number (e.g., +33123456789): ").strip()
    if not phone:
        print("[!] Phone number required.")
        input("Press Enter...")
        return
    data = lookup(phone)
    if data.get('valid'):
        print(f"Country: {data.get('country', 'N/A')}")
        print(f"Carrier: {data.get('carrier', 'N/A')}")
        print(f"Timezone(s): {', '.join(data.get('timezone', []))}")
    else:
        print(f"[!] Invalid or error: {data.get('error', 'Unknown')}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()