import subprocess
import os
import time

print("=" * 50)
print("УСТАНОВКА IVA CONNECT")
print("=" * 50)

installer = "C:\\Users\\s.antosenkov\\Downloads\\IVA Connect-25.4.6436.exe"

if os.path.exists(installer):
    print(f"Найден установщик: {installer}")
    
    # Завершаем старые процессы
    subprocess.run("taskkill /f /im IVA*.exe", shell=True, capture_output=True)
    time.sleep(2)
    
    # Правильные флаги для Inno Setup
    # /VERYSILENT - полная тихая установка
    # /SUPPRESSMSGBOXES - подавить все сообщения
    # /NORESTART - не перезагружать компьютер
    print("Запуск тихой установки...")
    
    # Используем run вместо Popen, чтобы дождаться завершения
    result = subprocess.run(f'"{installer}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART', shell=True)
    
    if result.returncode == 0:
        print("Установка успешно завершена!")
    else:
        print(f"Ошибка установки. Код возврата: {result.returncode}")
else:
    print("Установщик не найден!")

print("=" * 50)