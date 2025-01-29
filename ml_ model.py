import logging
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import time

class MLModel:
    """
    Модуль для работы с машинным обучением.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.model = None
        self.retrain_interval = 60 * 10  # Переобучение каждые 10 минут

    def build_model(self):
        """
        Построение гибридной модели LSTM + Transformer с оптимизацией.
        """
        inputs = tf.keras.Input(shape=(None, 1))  # Входные данные (временные ряды)

        # LSTM слой с оптимизацией
        lstm_out = tf.keras.layers.LSTM(128, return_sequences=True)(inputs)

        # Transformer слой с оптимизацией
        transformer_layer = tf.keras.layers.MultiHeadAttention(num_heads=4, key_dim=64)(lstm_out, lstm_out)
        transformer_out = tf.keras.layers.LayerNormalization()(transformer_layer)

        # Выходной слой
        outputs = tf.keras.layers.Dense(1)(transformer_out)

        model = tf.keras.Model(inputs, outputs)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="mse")
        self.model = model
        self.logger.info("Гибридная модель LSTM + Transformer успешно построена.")

    def load_model(self):
        """
        Загрузка предобученной модели.
        """
        try:
            self.model = tf.keras.models.load_model("models/pretrained_model.h5")
            self.logger.info("Предобученная модель успешно загружена.")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке модели: {e}")
            raise

    def save_model(self):
        """
        Сохранение обученной модели.
        """
        try:
            self.model.save("models/pretrained_model.h5")
            self.logger.info("Модель успешно сохранена.")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении модели: {e}")
            raise

    def retrain_model(self, new_data):
        """
        Переобучение модели на новых данных.
        """
        self.logger.info("Начало переобучения модели...")
        try:
            X, y = new_data['features'], new_data['labels']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Преобразование данных для LSTM
            X_train = np.array(X_train).reshape((X_train.shape[0], X_train.shape[1], 1))
            X_test = np.array(X_test).reshape((X_test.shape[0], X_test.shape[1], 1))

            self.model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test))
            self.logger.info("Модель успешно переобучена.")

            # Валидация модели
            predictions = self.model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            self.logger.info(f"MSE на тестовых данных: {mse}")

            # Сохранение модели после переобучения
            self.save_model()
        except Exception as e:
            self.logger.error(f"Ошибка при переобучении модели: {e}")
            raise