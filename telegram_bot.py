import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from modules.security import SecurityManager

class TelegramBot:
    """
    Модуль для управления ботом через Telegram.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.updater = None
        self.security_manager = SecurityManager()

    def start_bot(self):
        """
        Запуск Telegram-бота.
        """
        try:
            from config.config import TELEGRAM_BOT_TOKEN
            self.updater = Updater(TELEGRAM_BOT_TOKEN)
            dispatcher = self.updater.dispatcher

            # Регистрация команд
            dispatcher.add_handler(CommandHandler("start", self.start))
            dispatcher.add_handler(CommandHandler("status", self.status))
            dispatcher.add_handler(CommandHandler("balance", self.balance))
            dispatcher.add_handler(CommandHandler("trades", self.trades))
            dispatcher.add_handler(CommandHandler("profit", self.profit))

            self.updater.start_polling()
            self.logger.info("Telegram-бот успешно запущен.")
        except Exception as e:
            self.logger.error(f"Ошибка при запуске Telegram-бота: {e}")
            raise

    def start(self, update: Update, context: CallbackContext):
        """
        Команда /start.
        """
        user = update.effective_user
        update.message.reply_text(f"Привет, {user.first_name}! Бот запущен.")

    def status(self, update: Update, context: CallbackContext):
        """
        Команда /status.
        """
        if self.security_manager.is_authenticated():
            update.message.reply_text("Статус: Все системы работают нормально.")
        else:
            update.message.reply_text("Статус: Доступ запрещен.")

    def balance(self, update: Update, context: CallbackContext):
        """
        Команда /balance.
        """
        try:
            balances = self.get_account_balances()
            message = "\n".join([f"{key}: {value}" for key, value in balances.items()])
            update.message.reply_text(f"Балансы аккаунтов:\n{message}")
        except Exception as e:
            update.message.reply_text(f"Ошибка при получении балансов: {e}")

    def trades(self, update: Update, context: CallbackContext):
        """
        Команда /trades.
        """
        try:
            trades = self.get_recent_trades()
            message = "\n".join([f"{trade['symbol']}: {trade['amount']} {trade['side']}" for trade in trades])
            update.message.reply_text(f"Последние сделки:\n{message}")
        except Exception as e:
            update.message.reply_text(f"Ошибка при получении сделок: {e}")

    def profit(self, update: Update, context: CallbackContext):
        """
        Команда /profit.
        """
        try:
            profit = self.calculate_profit()
            update.message.reply_text(f"Текущая прибыль: {profit}%")
        except Exception as e:
            update.message.reply_text(f"Ошибка при расчете прибыли: {e}")

    def send_message(self, message):
        """
        Отправка сообщения через Telegram.
        """
        try:
            from config.config import TELEGRAM_CHAT_ID
            self.updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as e:
            self.logger.error(f"Ошибка при отправке сообщения: {e}")
            raise