# token_analysis/management/commands/populate_token_analysis.py

import time
import requests
from django.core.management.base import BaseCommand
from token_analysis.models import TokenAnalysis

class Command(BaseCommand):
    help = 'Populate the TokenAnalysis table using CoinGecko API'

    def handle(self, *args, **kwargs):
        base_url = 'https://api.coingecko.com/api/v3/coins/'

        # Fetch the list of coins
        list_url = base_url + 'list'
        response = requests.get(list_url)
        response.raise_for_status()
        coins = response.json()

        for coin in coins:
            coin_id = coin['id']
            coin_url = base_url + coin_id
            try:
                response = requests.get(coin_url)
                response.raise_for_status()
                data = response.json()

                token_data = {
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'symbol': data.get('symbol'),
                    'platform': data['asset_platform_id'],
                    'blocktime': data['block_time_in_minutes'],
                    'description': data['description']['en'],
                    'website': data['links']['homepage'][0] if data['links']['homepage'] else None,
                    'whitepaper': data['links']['whitepaper'][0] if data['links']['whitepaper'] else None,
                    'official_forum': data['links']['official_forum_url'][0] if data['links']['official_forum_url'] else None,
                    'announcement': data['links']['announcement_url'][0] if data['links']['announcement_url'] else None,
                    'twitter': data['links']['twitter_screen_name'],
                    'telegram': data['links']['telegram_channel_identifier'],
                    'reddit': data['links']['subreddit_url'],
                    'sentiment_votes_up': data['sentiment_votes_up_percentage'],
                    'sentiment_votes_down': data['sentiment_votes_down_percentage'],
                    'facebook_likes': data['community_data']['facebook_likes'],
                    'twitter_followers': data['community_data']['twitter_followers'],
                    'reddit_subscribers': data['community_data']['reddit_subscribers'],
                    'telegram_channel': data['community_data']['telegram_channel_user_count'],
                    'forks': data['developer_data']['forks'],
                    'stars': data['developer_data']['stars'],
                    'subscribers': data['developer_data']['subscribers'],
                    'total_issues': data['developer_data']['total_issues'],
                    'logo': data['image']['large'],  # Fetch and save the logo URL
                }

                TokenAnalysis.objects.update_or_create(
                    id=token_data['id'],
                    defaults=token_data
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully updated token {coin_id}'))

                time.sleep(1)  # Sleep to respect API rate limits

            except requests.exceptions.RequestException as e:
                self.stderr.write(f'Error fetching data for {coin_id}: {e}')
                time.sleep(10)  # Wait before retrying
