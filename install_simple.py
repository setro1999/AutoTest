import subprocess
import os

print("=" * 50)
print("СКРИПТ УСТАНОВКИ IVA CONNECT")
print("=" * 50)

# Точный путь к установщику
installer_path = "C:\\Users\\s.antosenkov\\Downloads\\IVA Connect-25.4.6436.exe"

print(f"1. Проверяем существование файла:")
print(f"   {installer_path}")

if os.path.exists(installer_path):
    print("   ФАЙЛ СУЩЕСТВУЕТ!")
    
    print(f"\n2. Проверяем права на чтение файла:")
    if os.access(installer_path, os.R_OK):
        print("   ФАЙЛ ДОСТУПЕН ДЛЯ ЧТЕНИЯ")
        
        print(f"\n3. Завершаем процессы IVA...")
        subprocess.run("taskkill /f /im IVA*.exe", shell=True, capture_output=True)
        
        print(f"\n4. Запускаем установку...")
        print(f"   Команда: {installer_path} /S /verysilent")
        
        try:
            result = subprocess.run(f'"{installer_path}" /S /verysilent', shell=True)
            print(f"   Результат: {result.returncode}")
            print("   УСТАНОВКА ЗАПУЩЕНА!")
        except Exception as e:
            print(f"   ОШИБКА: {e}")
    else:
        print("   НЕТ ПРАВ НА ЧТЕНИЕ!")
else:
    print("   ФАЙЛ НЕ НАЙДЕН!")
    
    print(f"\nПроверяем содержимое папки Downloads:")
    downloads_dir = "C:\\Users\\s.antosenkov\\Downloads"
    if os.path.exists(downloads_dir):
        files = os.listdir(downloads_dir)
        print(f"   Найдено файлов: {len(files)}")
        
        print(f"   Первые 10 файлов в папке:")
        for i, file in enumerate(files[:10]):
            print(f"     {i+1}. {file}")
        
        print(f"\n   Поиск файлов с 'IVA' в имени:")
        found = False
        for file in files:
            if "IVA" in file:
                print(f"     НАЙДЕН: {file}")
                found = True
        if not found:
            print("     ФАЙЛЫ С 'IVA' НЕ НАЙДЕНЫ")
    else:
        print(f"   Папка Downloads не существует!")

print("=" * 50)
