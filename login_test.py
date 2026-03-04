import subprocess
import os

def find_and_run_program(program_name):
    search_roots = [
        r'C:\Program Files',
        r'C:\Program Files (x86)',
        os.path.expanduser('~\\AppData\\Local'),
        os.path.expanduser('~\\AppData\\Roaming'),
        os.path.expanduser('~\\Desktop'),
    ]
    
    print(f"Ищем {program_name}...")
    
    for root in search_roots:
        for dirpath, dirnames, filenames in os.walk(root):
            if program_name in filenames:
                full_path = os.path.join(dirpath, program_name)
                print(f"Найдено: {full_path}")
                try:
                    subprocess.Popen([full_path])
                    print("Программа запущена!")
                    return True
                except Exception as e:
                    print(f"Ошибка запуска: {e}")
                    return False
    
    print(f"Программа {program_name} не найдена")
    return False
find_and_run_program("IVA Connect.exe")