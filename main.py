import logging
from modules.core import Core

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)

def main():
    logging.info("Запуск системы...")
    try:
        core = Core()
        core.initialize()
    except Exception as e:
        logging.error(f"Критическая ошибка при запуске: {e}")

if __name__ == "__main__":
    main()