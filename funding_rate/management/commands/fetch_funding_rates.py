# sentiment_analysis/management/commands/fetch_funding_rates.py
from django.core.management.base import BaseCommand
from funding_rate.models import FundingRate
import ccxt

class Command(BaseCommand):
    help = 'Fetch funding rates from multiple exchanges and store them in the database'

    def handle(self, *args, **options):
        # ['binance', 'bitmex', 'bybit', 'kraken', 'okx']
        exchanges = ['kraken', 'okx']
        symbols = symbols = [
                                'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'SOL/USDT',
                                'DOT/USDT', 'XRP/USDT', 'LTC/USDT', 'LINK/USDT', 'BCH/USDT',
                                'UNI/USDT', 'DOGE/USDT', 'AVAX/USDT', 'AXS/USDT', 'MATIC/USDT',
                                'SHIB/USDT', 'SAND/USDT'
                            ]  # Extend this list with more symbols
        
        for exchange_id in exchanges:
            exchange = getattr(ccxt, exchange_id)()
            for symbol in symbols:
                try:
                    funding_rate_data = exchange.fetch_funding_rate(symbol)
                    funding_rate = funding_rate_data['fundingRate']
                    # Calculate sentiment score based on funding rate
                    sentiment_score = self.calculate_sentiment_score(funding_rate)
                    FundingRate.objects.update_or_create(
                        symbol=symbol,
                        defaults={
                            'coin_name': symbol.split('/')[0],
                            'stablecoin': symbol.split('/')[1],
                            'funding_rate': funding_rate,
                            'exchange': exchange_id,
                            'sentiment_score': sentiment_score,
                        }
                    )
                except Exception as e:
                    print(f"Error fetching funding rate for {symbol} on {exchange_id}: {e}")

    def calculate_sentiment_score(self, funding_rate):
        if funding_rate > 0:
            return 1  # Bullish
        elif funding_rate < 0:
            return -1  # Bearish
        else:
            return 0  # Neutral
