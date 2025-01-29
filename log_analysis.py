import logging
from elasticsearch import Elasticsearch

class LogAnalyzer:
    """
    Модуль для анализа логов с использованием ELK Stack.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.es = Elasticsearch(["http://localhost:9200"])  # Замените на реальный адрес Elasticsearch

    def index_logs(self, log_data):
        """
        Индексация логов в Elasticsearch.
        """
        try:
            self.es.index(index="app-logs", body=log_data)
            self.logger.info("Логи успешно проиндексированы.")
        except Exception as e:
            self.logger.error(f"Ошибка при индексации логов: {e}")
            raise

    def search_logs(self, query):
        """
        Поиск логов в Elasticsearch.
        """
        try:
            response = self.es.search(index="app-logs", body=query)
            self.logger.info("Поиск логов выполнен успешно.")
            return response
        except Exception as e:
            self.logger.error(f"Ошибка при поиске логов: {e}")
            raise