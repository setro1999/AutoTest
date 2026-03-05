import logging
import subprocess
import time
import os
import pyautogui
import sys
import pydirectinput
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

log_dir = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = f"login_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_path = os.path.join(log_dir, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

LOGIN_DATA = {
    'username': os.getenv('IVA_USERNAME', ''),
    'password': os.getenv('IVA_PASSWORD', ''),
    'server': os.getenv('IVA_SERVER', '')
}

if not all(LOGIN_DATA.values()):
    logger.error("Ошибка: не все переменные окружения заданы в .env файле")
    sys.exit(1)

script_dir = os.path.dirname(__file__)
IMAGES = {
    'server_field': os.path.join(script_dir, 'images', 'server_field.png'),
    'continue_button': os.path.join(script_dir, 'images', 'continue_button.png'),
    'login_field': os.path.join(script_dir, 'images', 'login_field.png'),
    'password_field': os.path.join(script_dir, 'images', 'password_field.png'),
    'login_button': os.path.join(script_dir, 'images', 'login_button.png')
}

class TestIVALogin:
    
    def find_and_click(self, image_path, desc, timeout=30):
        logger.info(f"Поиск: {desc}")
        start = time.time()
        while time.time() - start < timeout:
            try:
                loc = pyautogui.locateOnScreen(image_path, confidence=0.7)
                if loc:
                    center = pyautogui.center(loc)
                    pydirectinput.click(center.x, center.y)
                    logger.info(f"Найден: {desc}")
                    time.sleep(1)
                    return True
            except:
                pass
            time.sleep(1)
        
        logger.error(f"Не найден: {desc}")
        return False
    
    def type_text_direct(self, text, field_desc):
        """Прямой ввод текста через pydirectinput"""
        logger.info(f"Ввод в {field_desc}: {text}")
        
        # Очищаем поле
        pydirectinput.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pydirectinput.press('delete')
        time.sleep(0.5)
        
        # Вводим текст посимвольно
        for char in text:
            if char == '@':
                pydirectinput.keyDown('shift')
                pydirectinput.press('2')
                pydirectinput.keyUp('shift')
            elif char == '.':
                pydirectinput.press('.')
            elif char == '-':
                pydirectinput.press('-')
            else:
                pydirectinput.write(char)
            time.sleep(0.05)
        
        logger.info(f"✅ Текст введен")
    
    def test_login(self):
        logger.info("=" * 50)
        logger.info("ТЕСТ АВТОРИЗАЦИИ")
        logger.info("=" * 50)
        
        # Завершаем старые процессы
        subprocess.run("taskkill /f /im IVA*.exe", shell=True, capture_output=True)
        time.sleep(3)
        
        # Запуск программы
        iva_path = "C:\\Program Files\\IVA Connect\\IVA Connect.exe"
        if not os.path.exists(iva_path):
            logger.error("Программа не найдена")
            return False
        
        subprocess.Popen([iva_path])
        logger.info("Программа запущена, ожидание 20 секунд...")
        time.sleep(20)
        
        # Ввод сервера
        if not self.find_and_click(IMAGES['server_field'], "поле сервера"):
            return False
        time.sleep(2)
        self.type_text_direct(LOGIN_DATA['server'], "сервер")
        time.sleep(2)
        
        # Кнопка продолжить
        if not self.find_and_click(IMAGES['continue_button'], "кнопка Продолжить"):
            return False
        time.sleep(5)
        
        # Ввод логина
        if not self.find_and_click(IMAGES['login_field'], "поле логина"):
            return False
        time.sleep(2)
        self.type_text_direct(LOGIN_DATA['username'], "логин")
        time.sleep(2)
        
        # Ввод пароля
        pydirectinput.press('tab')
        time.sleep(2)
        self.type_text_direct(LOGIN_DATA['password'], "пароль")
        time.sleep(2)
        
        # Нажатие кнопки Войти
        if not self.find_and_click(IMAGES['login_button'], "кнопка Войти", timeout=10):
            logger.warning("Кнопка Войти не найдена, пробуем Enter")
            pydirectinput.press('enter')
        
        time.sleep(10)
        
        # Проверка
        result = subprocess.run('tasklist /FI "IMAGENAME eq IVA Connect.exe"', 
                              shell=True, capture_output=True, text=True)
        
        if "IVA Connect.exe" in result.stdout:
            logger.info("=" * 50)
            logger.info("ТЕСТ УСПЕШЕН")
            logger.info("=" * 50)
            return True
        else:
            logger.error("=" * 50)
            logger.error("ТЕСТ ПРОВАЛЕН")
            logger.error("=" * 50)
            return False

if __name__ == "__main__":
    test = TestIVALogin()
    test.test_login()