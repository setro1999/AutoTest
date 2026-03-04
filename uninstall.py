import subprocess, os, shutil, winreg

def find_and_uninstall_program(program_name):
    print(f"Поиск {program_name} для удаления...")
    for uninstall_path in [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_path) as key:
                i = 0
                while True:
                    try:
                        with winreg.OpenKey(key, winreg.EnumKey(key, i)) as subkey:
                            try:
                                if program_name.replace(".exe", "") in winreg.QueryValueEx(subkey, "DisplayName")[0]:
                                    subprocess.run(winreg.QueryValueEx(subkey, "UninstallString")[0], shell=True)
                                    return True
                            except: pass
                        i += 1
                    except: break
        except: pass
    
    for root in [r'C:\Program Files', r'C:\Program Files (x86)', os.path.expanduser('~\\AppData\\Local'), os.path.expanduser('~\\AppData\\Roaming'), os.path.expanduser('~\\Desktop')]:
        if os.path.exists(root):
            for dirpath, _, filenames in os.walk(root):
                if program_name in filenames:
                    full_path = os.path.join(dirpath, program_name)
                    subprocess.run(f"taskkill /f /im {program_name}", shell=True, capture_output=True)
                    try: os.remove(full_path); os.rmdir(dirpath)
                    except: pass
                    return True
    return False

find_and_uninstall_program("IVA Connect.exe")