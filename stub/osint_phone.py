#!/usr/bin/env python3
import sys
import re

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

def lookup_phonenumbers(phone_str):
    if not PHONENUMBERS_AVAILABLE:
        return {"error": "phonenumbers module not installed"}
    try:
        number = phonenumbers.parse(phone_str, None)
        if not phonenumbers.is_valid_number(number):
            return {"error": "Invalid phone number"}
        return {
            "country": geocoder.description_for_number(number, "en") or "Unknown",
            "carrier": carrier.name_for_number(number, "en") or "Unknown",
            "timezone": ", ".join(timezone.time_zones_for_number(number)) or "Unknown",
            "valid": True
        }
    except Exception as e:
        return {"error": str(e)}

def lookup_veriphone(phone_str):
    try:
        import requests
        r = requests.get(f"https://api.veriphone.io/v2/verify?phone={phone_str}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return {
                    "country": data.get("country_name", "Unknown"),
                    "carrier": data.get("carrier", "Unknown"),
                    "valid": data.get("phone_valid", False)
                }
        return None
    except:
        return None

def lookup(phone_str):
    phone_str = re.sub(r'[^0-9+]', '', phone_str)
    if not phone_str:
        return {"error": "Empty phone number"}
    result = lookup_phonenumbers(phone_str)
    if "error" not in result:
        return {"source": "phonenumbers", "data": result}
    try:
        import requests
        result = lookup_veriphone(phone_str)
        if result:
            return {"source": "veriphone.io", "data": result}
    except:
        pass
    return {"error": "All services failed. Check the number format."}

def main():
    print("\n[SNOOP OSINT] Phone Number Lookup")
    phone = input("Enter phone number (e.g., +33123456789): ").strip()
    if not phone:
        print("[!] Phone number required.")
        input("Press Enter...")
        return
    print(f"\n[+] Looking up {phone}...")
    data = lookup(phone)
    if "error" in data:
        print(f"[!] Error: {data['error']}")
    else:
        print(f"Source: {data.get('source', 'Unknown')}")
        result = data.get('data', {})
        for k, v in result.items():
            print(f"{k}: {v}")
    input("\nPress Enter to return...")

if __name__ == "__main__":
    main()