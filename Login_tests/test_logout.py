import logging
import subprocess
import time
import os
import pyautogui
import sys
import pygetwindow as gw
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

log_dir = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = f"logout_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
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

script_dir = os.path.dirname(__file__)
IMAGES = {
    'profile_icon': os.path.join(script_dir, 'images', 'profile_icon.png'),
    'logout_button': os.path.join(script_dir, 'images', 'logout_button.png'),
    'confirm_logout': os.path.join(script_dir, 'images', 'confirm_logout.png'),
    'server_field': os.path.join(script_dir, 'images', 'server_field.png')
}

def focus_iva_window():
    try:
        windows = gw.getWindowsWithTitle('IVA Connect')
        if windows:
            win = windows[0]
            if win.isMinimized:
                win.restore()
                logger.info("Окно развернуто")
            win.activate()
            logger.info("Окно активировано")
            time.sleep(2)
            return True
        return False
    except Exception as e:
        logger.error(f"Ошибка фокусировки: {e}")
        return False

def find_and_click(image_path, desc, timeout=30):
    logger.info(f"Поиск: {desc}")
    start = time.time()
    
    while time.time() - start < timeout:
        try:
            loc = pyautogui.locateOnScreen(image_path, confidence=0.7)
            if loc:
                center = pyautogui.center(loc)
                pyautogui.click(center)
                logger.info(f"Найдено: {desc} в {center}")
                return True
        except:
            pass
        time.sleep(1)
    
    logger.error(f"Не найдено: {desc}")
    return False

def test_logout():
    logger.info("=" * 50)
    logger.info("ТЕСТ ВЫХОДА ИЗ СИСТЕМЫ")
    logger.info("=" * 50)
    
    # Проверка скриншотов
    for name, path in IMAGES.items():
        if not os.path.exists(path):
            logger.error(f"Нет скриншота: {path}")
            return False
    
    # Проверка процесса
    result = subprocess.run('tasklist /FI "IMAGENAME eq IVA Connect.exe"', 
                          shell=True, capture_output=True, text=True)
    
    if "IVA Connect.exe" not in result.stdout:
        logger.error("Программа не запущена")
        return False
    
    # Фокус на окно
    focus_iva_window()
    
    # Шаг 1: Клик по иконке профиля
    if not find_and_click(IMAGES['profile_icon'], "иконка профиля"):
        return False
    
    time.sleep(2)
    
    # Шаг 2: Клик по кнопке выхода
    if not find_and_click(IMAGES['logout_button'], "кнопка выхода"):
        return False
    
    time.sleep(2)
    
    # Шаг 3: Подтверждение выхода (кнопка Выйти в диалоговом окне)
    if not find_and_click(IMAGES['confirm_logout'], "подтверждение выхода"):
        logger.warning("Кнопка подтверждения не найдена, возможно выход без подтверждения")
    
    time.sleep(5)
    
    # Шаг 4: Проверка что попали на экран входа
    if find_and_click(IMAGES['server_field'], "поле сервера (проверка)", timeout=10):
        logger.info("=" * 50)
        logger.info("ТЕСТ УСПЕШЕН - ВЫХОД ВЫПОЛНЕН")
        logger.info("=" * 50)
        return True
    else:
        logger.error("=" * 50)
        logger.error("ТЕСТ ПРОВАЛЕН - НЕ УДАЛОСЬ ВЫЙТИ")
        logger.error("=" * 50)
        return False

if __name__ == "__main__":
    test_logout()