# populate_tokens via api from coingecko
# This implementation will continue to fetch and store tokens, page by page, until there are no more tokens to fetch. 
# It includes basic error handling and respects API rate limits by introducing a delay between requests.

import time
import requests
from django.core.management.base import BaseCommand
from sentiment_analysis.models import Token

class Command(BaseCommand):
    help = 'Populate the Token table using CoinGecko API'

    def handle(self, *args, **kwargs):
        url = 'https://api.coingecko.com/api/v3/coins/markets'
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': 1,
            'sparkline': 'false'
        }

        while True:
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break

                for item in data:
                    token, created = Token.objects.update_or_create(
                        symbol=item['symbol'],
                        defaults={
                            'name': item['name'],
                            'market_cap': item['market_cap'],
                            'price': item['current_price'],
                            'volume_24h': item['total_volume'],
                            'circulating_supply': item['circulating_supply'],
                            'max_supply': item['max_supply'] if item['max_supply'] else 0,
                            'logo': item['image'],  # Fetch and save the logo URL
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created token {token.name} ({token.symbol})'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated token {token.name} ({token.symbol})'))
                
                params['page'] += 1  # Go to the next page
                time.sleep(1)  # Sleep to respect API rate limits
                
            except requests.exceptions.RequestException as e:
                self.stderr.write(f'Error fetching data: {e}')
                time.sleep(10)  # Wait before retrying
