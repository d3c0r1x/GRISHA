import logging
from modules.data_handler import DataHandler
from modules.ml_model import MLModel
from modules.telegram_bot import TelegramBot
from modules.security import SecurityManager
from modules.account_manager import AccountManager
from modules.websocket_handler import WebSocketHandler
from modules.load_testing import LoadTester

class Core:
    """
    Ядро системы, отвечающее за инициализацию всех модулей.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data_handler = DataHandler()
        self.ml_model = MLModel()
        self.telegram_bot = TelegramBot()
        self.security_manager = SecurityManager()
        self.account_manager = AccountManager()
        self.websocket_handler = WebSocketHandler()
        self.load_tester = LoadTester()

    def initialize(self):
        """
        Инициализация всех компонентов системы.
        """
        self.logger.info("Инициализация ядра...")
        self.security_manager.authenticate()  # Проверка безопасности
        self.data_handler.load_config()
        self.ml_model.load_model()
        self.telegram_bot.start_bot()
        self.account_manager.load_accounts()
        self.websocket_handler.connect_websockets()
        self.load_tester.run_load_tests()
        self.logger.info("Система успешно инициализирована.")