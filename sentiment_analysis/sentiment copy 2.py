import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from .models import Token, Sentiment

# Twitter scraping setup
def fetch_tweets(token_symbol):
    url = f'https://x.com/search?q=%23{token_symbol}&src=typed_query'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tweets = [p.text for p in soup.find_all('p', {'class': 'tweet-text'})]
    return tweets[:100]

# Reddit scraping setup
def fetch_reddit_posts(token_symbol):
    url = f'https://www.reddit.com/search/?q={token_symbol}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    posts = [div.text for div in soup.find_all('div', {'class': 'scrollerItem'})]
    return posts[:100]

# Altcoinstalks scraping setup
def fetch_altcoinstalks_posts(token_symbol):
    url = f'https://www.altcoinstalks.com/index.php?topic={token_symbol}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        posts = soup.find_all('div', class_='post')
        return [post.get_text() for post in posts]
    return []

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def save_sentiments(token_symbol):
    tokens = Token.objects.filter(symbol=token_symbol)
    
    if not tokens.exists():
        print(f"Token {token_symbol} does not exist in the database.")
        return

    sources = {
        'Twitter': fetch_tweets,
        'Reddit': fetch_reddit_posts,
        'Altcoinstalks': fetch_altcoinstalks_posts,
    }

    for token in tokens:
        print(f"Processing token: {token.symbol}")
        for source, fetch_function in sources.items():
            messages = fetch_function(token_symbol)
            if not messages:
                print(f"No messages found for {token_symbol} from {source}")
                continue
            
            print(f"Found {len(messages)} messages for {token_symbol} from {source}")

            for message in messages:
                sentiment_score = analyze_sentiment(message)
                print(f"Message: {message}")
                print(f"Sentiment score: {sentiment_score}")
                Sentiment.objects.update_or_create(
                    token=token,
                    text=message,
                    source=source,
                    defaults={'sentiment_score': sentiment_score}
                )
                print(f"Saved sentiment for message: {message}")

