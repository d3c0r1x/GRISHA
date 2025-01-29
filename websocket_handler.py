import logging
import asyncio
import websockets
import json

class WebSocketHandler:
    """
    Модуль для работы с WebSocket для ускорения сделок.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.uri = "wss://stream.binance.com:9443/ws/btcusdt@ticker"  # Пример для Binance
        self.websocket = None

    async def connect_websocket(self):
        """
        Подключение к WebSocket.
        """
        try:
            async with websockets.connect(self.uri) as ws:
                self.websocket = ws
                self.logger.info("WebSocket успешно подключен.")
                await self.listen_websocket()
        except Exception as e:
            self.logger.error(f"Ошибка при подключении к WebSocket: {e}")
            raise

    async def listen_websocket(self):
        """
        Прослушивание WebSocket для получения данных в реальном времени.
        """
        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)
                self.logger.info(f"Получены данные через WebSocket: {data}")
                # Здесь можно добавить обработку данных для арбитража или торговли
        except Exception as e:
            self.logger.error(f"Ошибка при прослушивании WebSocket: {e}")
            raise

    def connect_websockets(self):
        """
        Запуск WebSocket в отдельном потоке.
        """
        try:
            asyncio.run(self.connect_websocket())
        except Exception as e:
            self.logger.error(f"Ошибка при запуске WebSocket: {e}")
            raise