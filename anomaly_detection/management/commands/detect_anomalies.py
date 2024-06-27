import requests
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from django.core.management.base import BaseCommand
from django.utils import timezone
from anomaly_detection.models import Anomaly, RiskAssessment

class Command(BaseCommand):
    help = 'Detect anomalies in cryptocurrency data'

    def fetch_market_data(self, crypto_id):
        url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
        params = {
            'vs_currency': 'usd',
            'days': 365, #max
            'interval': 'daily'
        }

        response = requests.get(url, params=params)
        data = response.json()

        # Debugging: Print the keys in the response
        print(f"Response keys for {crypto_id}: {data.keys()}")

        if 'prices' not in data or 'total_volumes' not in data:
            raise ValueError(f"Missing expected keys in API response for {crypto_id}")

        prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
        return pd.merge(prices, volumes, on='timestamp')

    def preprocess_data(self, data):
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['timestamp'] = data['timestamp'].apply(lambda x: timezone.make_aware(x, timezone.get_current_timezone()))
        data.set_index('timestamp', inplace=True)
        return data

    def detect_anomalies(self, data):
        model = IsolationForest(contamination=0.01)
        data['anomaly'] = model.fit_predict(data[['price', 'volume']])
        data['anomaly'] = data['anomaly'].map({1: 0, -1: 1})
        return data

    def plot_anomalies(self, data, crypto_id):
        anomalies = data[data['anomaly'] == 1]
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['price'], label='Price')
        plt.scatter(anomalies.index, anomalies['price'], color='red', label='Anomalies')
        plt.title(f'Price Anomalies for {crypto_id}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        subfolder = os.path.join('static', 'anomaly')
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        plt.savefig(os.path.join(subfolder, f'anomalies_{crypto_id}.png'))
        plt.close()

    def handle(self, *args, **kwargs):
        list_url = 'https://api.coingecko.com/api/v3/coins/list'
        list_response = requests.get(list_url)
        list_data = list_response.json()

        for crypto in list_data:
            crypto_id = crypto['id']
            try:
                data = self.fetch_market_data(crypto_id)
                data = self.preprocess_data(data)
                data = self.detect_anomalies(data)

                for _, row in data.iterrows():
                    Anomaly.objects.update_or_create(
                        crypto_id=crypto_id,
                        timestamp=row.name,
                        defaults={
                            'price': row['price'],
                            'volume': row['volume'],
                            'is_anomaly': bool(row['anomaly'])
                        }
                    )

                self.plot_anomalies(data, crypto_id)

                self.stdout.write(self.style.SUCCESS(f'Processed {crypto_id}'))

                time.sleep(1)  # Respect API rate limits

            except requests.exceptions.RequestException as e:
                self.stderr.write(f'Error fetching data for {crypto_id}: {e}')
                time.sleep(10)  # Wait before retrying
            except ValueError as ve:
                self.stderr.write(f'Error processing data for {crypto_id}: {ve}')
