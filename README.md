# 🛠️ Snoop - Multi-Tools

**A comprehensive security research and penetration testing toolkit.**

---

## ⚠️ DISCLAIMER

> **This tool is strictly for educational purposes and authorized penetration testing only.**
>
> Unauthorized access to computer systems, networks, or accounts is illegal. The author (weaselgb) does not condone or take responsibility for any misuse of this software. By downloading, installing, or using this tool, you agree that you are solely responsible for your actions and will use it exclusively on systems you own or have explicit written permission to test.

---

## ✨ Features

Snoop is a modular framework with over **40+ built-in tools**, organized into 7 main categories:

### 1. 🧨 Malicious Tools
| Tool | Description |
| :--- | :--- |
| **Grabber** | Steal browser passwords, cookies, Discord tokens, and system info. |
| **RAT** | Full remote access (execute commands, transfer files, capture screen). |
| **IP Grabber** | Log IP addresses, geolocation, ISP, and system data. |
| **Keylogger** | Record keystrokes and send logs via webhook. |
| **Crypto Scanner** | Scan for cryptocurrency wallet files and private keys. |
| **Mail Bomber** | Flood email inboxes with spam messages. |
| **DDoS Attack** | Layer 7 HTTP flood and Layer 4 SYN flood. |
| **Vuln Scanner** | Detect common web vulnerabilities (SQLi, XSS, etc.). |
| **Blocker** | Self-destructing persistence with remote command control. |

### 2. 💬 Discord Tools
- Selfbot (with commands)
- Raid / Nuke (mass ban, channel creation, etc.)
- Webhook Spam / Delete
- Token Info / Login / Nuker / Rotator / Onliner
- ID to Token (convert user ID to token)
- Server Cloner
- Server Info from Invite
- Username Checker
- Report Bot
- Bot Invite Generator

### 3. 🔎 OSINT Tools
- IP Lookup (geolocation, ISP, ASN)
- Email Lookup (breach data, social media)
- Phone Lookup (carrier, location, validity)
- Username Tracker (across platforms)
- Whois Lookup (domain registration)
- DNS Enumeration (records, zone transfer)
- Subdomain Finder
- Port Scanner (common ports)
- Shodan Search (device info)
- Wayback Machine (historical snapshots)
- Social Scraper (profiles from usernames)
- Email Verifier (SMTP, MX)
- Pastebin Dorking (search leaks)
- GeoIP Location (coordinates, map)
- Dox Creator (compile public data)

### 4. 🧰 Tools
- **Binder** – Combine two EXEs into one.
- **Crypter** – XOR-encrypt an EXE with a loader.
- **Fusion** – Combine Grabber and RAT into one payload.
- **Crypted RAT** – Encrypted RAT with loader.
- **Crypted Grabber** – Encrypted Grabber with loader.
- **USB Worm** – Auto-copy payload to USB drives.
- **Network Scanner** – Discover hosts and open ports on a LAN.
- **Phishing Page** – Generate a login page with credential logger.
- **Proxy Scraper** – Fetch fresh proxies from multiple sources.
- **Proxy Checker** – Test proxy speed and anonymity.
- **Website Cloner** – Download a full website (HTML, CSS, JS).
- **Python Obfuscator** – Obfuscate Python scripts.

### 5. 🔑 Login Tools
- **Token Login** – Inject Discord token into browser.
- **Cookie Login** – Inject cookies into any website.

### 6. 🎮 Roblox Tools
- User Info (profile, friends, groups)
- Cookie Info (extract data from `.ROBLOSECURITY`)
- Cookie Login (automate login)
- Cookie Refresher (refresh cookies)
- Group Info (members, ranks, shout)
- Asset Download (download models, audios)
- Name History (past usernames)
- Username Checker (availability)
- Generate Usernames (suggest available names)

### 7. ⚙️ Settings
- Clear saved configuration (tokens, channels, etc.)

---

## 📦 Installation

Install dependencies:

bash
pip install -r requirements.txt
Run the tool:

bash
python main.py

### ⚡ One-Click Install (Windows only)
For the absolute easiest setup:

1. Download or clone this repository.
2. Double-click the **`install.bat`** file located in the root folder.
3. The script will automatically:
   - Check if Python is installed.
   - Install all required dependencies from `requirements.txt`.
   - Launch Snoop immediately after installation.

> *No terminal commands needed – just double-click and go!*

---

### 🐍 Manual Installation (All Platforms)

#### Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)

#### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/weaselgb/Snoop---Multi-Tools.git
   cd Snoop---Multi-Tools
