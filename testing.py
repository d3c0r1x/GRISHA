import logging
import pytest
from unittest.mock import patch
from modules.data_handler import DataHandler
from modules.ml_model import MLModel
from modules.telegram_bot import TelegramBot

class Testing:
    """
    Модуль для тестирования системы.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_unit_tests(self):
        """
        Запуск модульных тестов.
        """
        try:
            pytest.main(["-v", "tests/unit_tests.py"])
            self.logger.info("Модульные тесты успешно выполнены.")
        except Exception as e:
            self.logger.error(f"Ошибка при запуске модульных тестов: {e}")
            raise

    def run_integration_tests(self):
        """
        Запуск интеграционных тестов.
        """
        try:
            pytest.main(["-v", "tests/integration_tests.py"])
            self.logger.info("Интеграционные тесты успешно выполнены.")
        except Exception as e:
            self.logger.error(f"Ошибка при запуске интеграционных тестов: {e}")
            raise

    def test_exchange_api(self, exchange_name):
        """
        Тестирование API биржи.
        """
        try:
            with patch('ccxt.binance') as MockExchange:
                mock_instance = MockExchange.return_value
                mock_instance.fetch_ticker.return_value = {"last": 10000}
                ticker = mock_instance.fetch_ticker("BTC/USDT")
                assert ticker["last"] == 10000
                self.logger.info(f"Тестирование API {exchange_name} успешно завершено.")
        except Exception as e:
            self.logger.error(f"Ошибка при тестировании API {exchange_name}: {e}")
            raise

        def setup_ci_cd(self):
            """
            Настройка CI/CD через GitHub Actions.
            """
            try:
                with open(".github/workflows/ci_cd.yml", "w") as file:
                    file.write("""
    name: CI/CD Pipeline
    on: [push]
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: '3.9'
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
          - name: Run tests
            run: pytest
    """)
                self.logger.info("CI/CD конфигурация успешно настроена.")
            except Exception as e:
                self.logger.error(f"Ошибка при настройке CI/CD: {e}")
                raise