import logging
from ccxt import kucoin, bybit, huobi, okx, gateio, exmo, bitget, mexc


class Arbitrage:
    """
    Модуль для реализации методов арбитража.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.exchanges = {}

    def load_exchanges(self):
        """
        Загрузка бирж из конфигурационного файла.
        """
        try:
            with open("config/config.yaml", "r") as file:
                config = yaml.safe_load(file)

            enabled_exchanges = config["enabled_exchanges"]
            api_keys = config["api_keys"]

            for exchange_name, enabled in enabled_exchanges.items():
                if enabled and exchange_name in api_keys:
                    for account_idx in range(1, 3):  # Два аккаунта для каждой биржи
                        account_key = f"account_{account_idx}"
                        for api_idx, api_set in enumerate(api_keys[exchange_name][account_key]):
                            unique_key = f"{exchange_name}_{account_key}_api{api_idx + 1}"
                            if exchange_name == "kucoin":
                                self.exchanges[unique_key] = kucoin({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "bybit":
                                self.exchanges[unique_key] = bybit({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "huobi":
                                self.exchanges[unique_key] = huobi({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "okx":
                                self.exchanges[unique_key] = okx({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                    "password": api_set["passphrase"],
                                })
                            elif exchange_name == "gateio":
                                self.exchanges[unique_key] = gateio({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "exmo":
                                self.exchanges[unique_key] = exmo({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "bitget":
                                self.exchanges[unique_key] = bitget({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
                            elif exchange_name == "mexc":
                                self.exchanges[unique_key] = mexc({
                                    "apiKey": api_set["api_key"],
                                    "secret": api_set["secret"],
                                })
            self.logger.info("Биржи успешно загружены.")
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке бирж: {e}")
            raise

    def find_price_difference(self, symbol):
        """
        Поиск разницы в ценах между биржами (межбиржевой арбитраж).
        """
        try:
            prices = {}
            for exchange_name, exchange in self.exchanges.items():
                ticker = exchange.fetch_ticker(symbol)
                prices[exchange_name] = ticker["last"]

            price_diff = max(prices.values()) - min(prices.values())
            self.logger.info(f"Разница в ценах для {symbol}: {price_diff}")
            return price_diff
        except Exception as e:
            self.logger.error(f"Ошибка при поиске разницы в ценах: {e}")
            raise