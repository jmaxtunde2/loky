# token_analysis/management/commands/scrape_whitepapers.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrape whitepaper URLs from whitepaper.io'

    def handle(self, *args, **kwargs):
        base_url = 'https://whitepaper.io/coins'
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        whitepapers = []

        for coin in soup.select('.whitepaper-card'):
            project_name = coin.select_one('.whitepaper-card-title').text.strip()
            whitepaper_url = coin.select_one('.whitepaper-card-button')['href']

            whitepapers.append({
                'project_name': project_name,
                'category': 'N/A',  # Whitepaper.io doesn't provide a category
                'whitepaper_url': whitepaper_url
            })
        df = pd.DataFrame(whitepapers)
        df.to_csv('whitepapers_io.csv', index=False)
        self.stdout.write(self.style.SUCCESS(f'Scraped {len(df)} whitepapers.'))
