import logging
from prometheus_client import start_http_server, Gauge
from modules.telegram_bot import TelegramBot

class Monitoring:
    """
    Модуль для мониторинга системы и отправки оповещений.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.telegram_bot = TelegramBot()
        self.metrics = {
            "system_uptime": Gauge("system_uptime", "System uptime in seconds"),
            "model_accuracy": Gauge("model_accuracy", "Accuracy of the ML model"),
            "api_latency": Gauge("api_latency", "Latency of API calls"),
        }

    def start_prometheus_server(self, port=8000):
        """
        Запуск Prometheus сервера для экспорта метрик.
        """
        try:
            start_http_server(port)
            self.logger.info(f"Prometheus сервер запущен на порту {port}.")
        except Exception as e:
            self.logger.error(f"Ошибка при запуске Prometheus сервера: {e}")
            raise

    def update_metrics(self, uptime, accuracy, latency):
        """
        Обновление метрик для мониторинга.
        """
        try:
            self.metrics["system_uptime"].set(uptime)
            self.metrics["model_accuracy"].set(accuracy)
            self.metrics["api_latency"].set(latency)
            self.logger.info("Метрики успешно обновлены.")
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении метрик: {e}")
            raise

    def send_alert(self, message):
        """
        Отправка оповещения через Telegram.
        """
        try:
            self.telegram_bot.send_message(message)
            self.logger.info(f"Оповещение отправлено: {message}")
        except Exception as e:
            self.logger.error(f"Ошибка при отправке оповещения: {e}")
            raise