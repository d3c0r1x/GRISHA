import logging
import tweepy
import praw
import requests
import pandas as pd
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA

class Analytics:
    """
    Модуль для анализа новостей, макроэкономических данных и временных рядов.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.twitter_api = None
        self.reddit_api = None

    def setup_twitter(self, api_key, api_secret, access_token, access_token_secret):
        """
        Настройка Twitter API.
        """
        try:
            auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
            self.twitter_api = tweepy.API(auth)
            self.logger.info("Twitter API успешно настроено.")
        except Exception as e:
            self.logger.error(f"Ошибка при настройке Twitter API: {e}")
            raise

    def fetch_tweets(self, query, count=100):
        """
        Получение твитов по запросу.
        """
        try:
            tweets = self.twitter_api.search_tweets(q=query, count=count)
            tweet_texts = [tweet.text for tweet in tweets]
            self.logger.info(f"Получено {len(tweet_texts)} твитов.")
            return tweet_texts
        except Exception as e:
            self.logger.error(f"Ошибка при получении твитов: {e}")
            raise

    def setup_reddit(self, client_id, client_secret, user_agent):
        """
        Настройка Reddit API.
        """
        try:
            self.reddit_api = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            self.logger.info("Reddit API успешно настроено.")
        except Exception as e:
            self.logger.error(f"Ошибка при настройке Reddit API: {e}")
            raise

    def fetch_reddit_posts(self, subreddit_name, limit=100):
        """
        Получение постов с Reddit.
        """
        try:
            subreddit = self.reddit_api.subreddit(subreddit_name)
            posts = [post.title for post in subreddit.hot(limit=limit)]
            self.logger.info(f"Получено {len(posts)} постов с Reddit.")
            return posts
        except Exception as e:
            self.logger.error(f"Ошибка при получении постов с Reddit: {e}")
            raise

    def analyze_news_sentiment(self, texts):
        """
        Анализ тональности новостей.
        """
        try:
            from textblob import TextBlob
            sentiments = [TextBlob(text).sentiment.polarity for text in texts]
            average_sentiment = sum(sentiments) / len(sentiments)
            self.logger.info(f"Средняя тональность новостей: {average_sentiment}")
            return average_sentiment
        except Exception as e:
            self.logger.error(f"Ошибка при анализе тональности: {e}")
            raise

    def cluster_data(self, data, n_clusters=3):
        """
        Кластеризация данных с использованием KMeans.
        """
        try:
            kmeans = KMeans(n_clusters=n_clusters)
            clusters = kmeans.fit_predict(data)
            self.logger.info(f"Данные успешно кластеризованы. Количество кластеров: {n_clusters}")
            return clusters
        except Exception as e:
            self.logger.error(f"Ошибка при кластеризации данных: {e}")
            raise

    def analyze_time_series(self, data):
        """
        Анализ временных рядов с использованием ARIMA.
        """
        try:
            model = ARIMA(data, order=(5, 1, 0))
            results = model.fit()
            forecast = results.forecast(steps=10)
            self.logger.info(f"Прогноз временного ряда: {forecast}")
            return forecast
        except Exception as e:
            self.logger.error(f"Ошибка при анализе временного ряда: {e}")
            raise