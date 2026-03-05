import time
import os
import sys

def wait_for_install():
    print("Ожидание завершения установки IVA Connect...")
    
    iva_path = "C:\\Program Files\\IVA Connect\\IVA Connect.exe"
    max_wait = 60  # теперь хватит 60 секунд, так как установка синхронная
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        if os.path.exists(iva_path):
            size = os.path.getsize(iva_path)
            print(f"ПРОГРАММА УСТАНОВЛЕНА! Размер: {size} байт")
            return 0
        
        elapsed = int(time.time() - start_time)
        print(f"Прошло {elapsed} сек. Ожидание...")
        time.sleep(2)
    
    print(f"ТАЙМАУТ {max_wait} секунд. Программа не установлена")
    return 1

if __name__ == "__main__":
    result = wait_for_install()
    sys.exit(result)