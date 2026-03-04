import subprocess, os
from pathlib import Path

def install_iva():
    for root in [str(Path.home() / "Downloads"), "C:\\Users\\s.antosenkov\\Downloads", "C:\\Users\\s.antosenkov\\Desktop"]:
        for file in os.listdir(root):
            if "IVA" in file and (file.endswith(".exe") or file.endswith(".msi")):
                path = os.path.join(root, file)
                subprocess.run("taskkill /f /im IVA*.exe", shell=True, capture_output=True)
                subprocess.run(f'"{path}" /S /verysilent' if path.endswith(".exe") else f'msiexec /i "{path}" /quiet', shell=True)
                print(f"Установка {file} запущена")
                return True
    print("Установщик не найден")
    return False

install_iva()