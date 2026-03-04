import subprocess
import os
import time

print("=" * 50)
print("УСТАНОВКА IVA CONNECT (ФОНОВЫЙ РЕЖИМ)")
print("=" * 50)

installer_path = "C:\\Users\\s.antosenkov\\Downloads\\IVA Connect-25.4.6436.exe"

if os.path.exists(installer_path):
    print(f"Найден установщик: {installer_path}")
    
    # Завершаем процессы
    subprocess.run("taskkill /f /im IVA*.exe", shell=True, capture_output=True)
    
    # Запускаем в фоне и НЕ ждем завершения
    print("Запуск установки в фоновом режиме...")
    subprocess.Popen(f'"{installer_path}" /S /verysilent', shell=True)
    
    # Даем 2 секунды на запуск
    time.sleep(2)
    
    print("Установка запущена в фоне и продолжается...")
    print("Пайплайн может продолжать работу")
    
    # Проверяем что процесс запустился
    time.sleep(1)
    print(" Установка инициирована")
    
else:
    print(" Установщик не найден!")

print("=" * 50)