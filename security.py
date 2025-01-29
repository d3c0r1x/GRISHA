import logging
import hashlib
import time
from cryptography.fernet import Fernet

class SecurityManager:
    """
    Модуль для обеспечения безопасности системы.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.authenticated = False
        self.last_auth_time = 0
        self.key = b'your-encryption-key-here'  # Ключ шифрования (замените на реальный)

    def authenticate(self):
        """
        Проверка аутентификации пользователя.
        """
        current_time = time.time()
        if current_time - self.last_auth_time > 4 * 3600:  # 4 часа
            password = input("Введите пароль: ")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == "your-hashed-password":  # Замените на реальный хеш
                self.authenticated = True
                self.last_auth_time = current_time
                self.logger.info("Аутентификация успешна.")
            else:
                self.logger.error("Неверный пароль.")
                raise PermissionError("Неверный пароль.")
        else:
            self.logger.info("Пользователь уже аутентифицирован.")

    def is_authenticated(self):
        """
        Проверка текущего статуса аутентификации.
        """
        return self.authenticated

    def encrypt_data(self, data):
        """
        Шифрование чувствительных данных.
        """
        try:
            cipher_suite = Fernet(self.key)
            encrypted_data = cipher_suite.encrypt(data.encode())
            self.logger.info("Данные успешно зашифрованы.")
            return encrypted_data
        except Exception as e:
            self.logger.error(f"Ошибка при шифровании данных: {e}")
            raise

    def decrypt_data(self, encrypted_data):
        """
        Дешифровка чувствительных данных.
        """
        try:
            cipher_suite = Fernet(self.key)
            decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
            self.logger.info("Данные успешно дешифрованы.")
            return decrypted_data
        except Exception as e:
            self.logger.error(f"Ошибка при дешифровке данных: {e}")
            raise

    def run_security_audit(self):
        """
        Анализ кода на уязвимости с использованием Bandit.
        """
        try:
            self.logger.info("Запуск анализа кода на уязвимости...")
            import subprocess
            result = subprocess.run(["bandit", "-r", "."], capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("Анализ кода завершен успешно. Уязвимостей не обнаружено.")
            else:
                self.logger.warning(f"Обнаружены потенциальные уязвимости:\n{result.stdout}")
        except Exception as e:
            self.logger.error(f"Ошибка при запуске анализа кода: {e}")
            raise