import requests
import time
from textblob import TextBlob
from .models import Token, Sentiment
from django.db import transaction, OperationalError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_coin_data(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data for {crypto_id}: {response.status_code}")
        print(f"URL: {url}")
        print(f"Response: {response.text}")
        return None

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def save_sentiments(token_symbol, retries=5, delay=5):
    tokens = Token.objects.filter(symbol=token_symbol)
    
    if not tokens.exists():
        print(f"Token {token_symbol} does not exist in the database.")
        return

    for token in tokens:
        crypto_id = token.crypto_id
        print(f"Processing token: {token.symbol} with CoinGecko ID: {crypto_id}")

        data = fetch_coin_data(crypto_id)
        if not data:
            print(f"No data found for {token_symbol} (ID: {crypto_id}) from CoinGecko")
            continue

        print(f"Found data for {token_symbol} (ID: {crypto_id}) from CoinGecko")

        community_data = data.get('community_data', {})
        if not community_data:
            print(f"No community data found for {token_symbol} (ID: {crypto_id}) from CoinGecko")
            continue

        community_texts = [
            f"Twitter followers: {community_data.get('twitter_followers', '')}",
            f"Reddit average posts (48h): {community_data.get('reddit_average_posts_48h', '')}",
            f"Reddit average comments (48h): {community_data.get('reddit_average_comments_48h', '')}",
            f"Reddit subscribers: {community_data.get('reddit_subscribers', '')}",
            f"Reddit accounts active (48h): {community_data.get('reddit_accounts_active_48h', '')}",
        ]

        for text in community_texts:
            if text:
                sentiment_score = analyze_sentiment(text)
                print(f"Community text: {text}")
                print(f"Sentiment score: {sentiment_score}")
                for attempt in range(retries):
                    try:
                        with transaction.atomic():
                            Sentiment.objects.update_or_create(
                                token=token,
                                text=text,
                                source="CoinGecko",
                                defaults={'sentiment_score': sentiment_score}
                            )
                        print(f"Saved sentiment for community text: {text}")
                        break
                    except OperationalError as e:
                        if attempt < retries - 1:
                            print(f"Database is locked, retrying in {delay} seconds...")
                            time.sleep(delay)
                        else:
                            logger.error(f"Failed to save sentiment after {retries} attempts: {e}")
                            raise

        time.sleep(10)  # Respect the API rate limit

# Example usage
# save_sentiments('btc')
