# sentiment_analysis/management/commands/fetch_bitcoin_sentiment.py
import requests
from django.core.management.base import BaseCommand
from sentiment_analysis.models import BitcoinSentiment

class Command(BaseCommand):
    help = 'Fetch Bitcoin sentiment data from Senticrypt API and store it in the database'

    def handle(self, *args, **options):
        url = 'https://api.senticrypt.com/v2/all.json'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                sentiment, created = BitcoinSentiment.objects.update_or_create(
                    date=entry['date'],
                    defaults={
                        'price': entry['price'],
                        'volume': entry['volume'],
                        'score1': entry['score1'],
                        'score2': entry['score2'],
                        'score3': entry['score3'],
                        'sum': entry['sum'],
                        'mean': entry['mean'],
                        'count': entry['count']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created sentiment for {entry["date"]}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Successfully updated sentiment for {entry["date"]}'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from Senticrypt API'))
