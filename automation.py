import logging
import schedule
import time
import requests
from icalendar import Calendar
from modules.data_handler import DataHandler

class Automation:
    """
    Модуль для автоматизации задач, таких как обновление данных и интеграция с календарями событий.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data_handler = DataHandler()

    def update_market_data(self):
        """
        Обновление рыночных данных с внешнего API.
        """
        try:
            response = requests.get("https://api.example.com/market-data")  # Замените на реальный API
            if response.status_code == 200:
                market_data = response.json()
                self.data_handler.save_data(market_data, "market_data")
                self.logger.info("Рыночные данные успешно обновлены.")
            else:
                self.logger.error(f"Ошибка при получении рыночных данных: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении рыночных данных: {e}")

    def fetch_calendar_events(self):
        """
        Получение экономических событий из iCalendar.
        """
        try:
            calendar_url = "https://example.com/calendar.ics"  # Замените на реальный URL
            response = requests.get(calendar_url)
            if response.status_code == 200:
                calendar = Calendar.from_ical(response.text)
                events = []
                for component in calendar.walk():
                    if component.name == "VEVENT":
                        event = {
                            "summary": str(component.get("summary")),
                            "start": str(component.get("dtstart").dt),
                            "end": str(component.get("dtend").dt),
                        }
                        events.append(event)
                self.data_handler.save_data(events, "calendar_events")
                self.logger.info("Календарные события успешно загружены.")
            else:
                self.logger.error(f"Ошибка при получении календарных событий: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке календарных событий: {e}")

    def update_dependencies(self):
        """
        Автоматическое обновление зависимостей через pip.
        """
        try:
            self.logger.info("Начинаю обновление зависимостей...")
            subprocess.run(["pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
            self.logger.info("Зависимости успешно обновлены.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Ошибка при обновлении зависимостей: {e}")
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка при обновлении зависимостей: {e}")

    def schedule_tasks(self):
        """
        Планирование задач для автоматического выполнения.
        """
        self.logger.info("Начинаю планирование задач...")
        schedule.every(1).hours.do(self.update_market_data)  # Обновление рыночных данных каждый час
        schedule.every().day.at("08:00").do(self.fetch_calendar_events)  # Загрузка событий каждое утро
        schedule.every().monday.at("00:00").do(self.update_dependencies)  # Обновление зависимостей каждую неделю

        while True:
            schedule.run_pending()
            time.sleep(1)