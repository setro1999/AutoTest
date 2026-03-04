import os
import subprocess
import time

print("=" * 50)
print("ПРОВЕРКА УСТАНОВКИ IVA CONNECT")
print("=" * 50)

# Пути где может быть установлена программа
paths = [
    r"C:\Program Files\IVA Connect\IVA Connect.exe",
    r"C:\Program Files (x86)\IVA Connect\IVA Connect.exe"
]

found = False

for path in paths:
    print(f"Проверка пути: {path}")
    if os.path.exists(path):
        print(f"   ФАЙЛ НАЙДЕН: {path}")
        
        # Проверяем размер файла
        size = os.path.getsize(path)
        print(f"  Размер файла: {size} байт")
        
        if size > 1000:
            print("   Файл корректен")
            found = True
            break
        else:
            print("  ❌ Файл слишком маленький")
    else:
        print("  ❌ Файл не найден")

if found:
    print("\n IVA Connect успешно установлен!")
else:
    print("\n IVA Connect НЕ установлен!")

print("=" * 50)