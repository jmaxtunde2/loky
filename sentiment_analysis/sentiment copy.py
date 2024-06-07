import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from .models import Token,Sentiment

#function to scrab tweet from twitter
def fetch_tweets(symbol,count = 100):
    url = f"https://x.com/search?q={symbol}&src=typed_query"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = [p.text for p in soup.find_all('p', {'class': 'tweet-text'})][:count]
    return tweets

# function to analyse sentiment 
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

#function to save sentiments
def save_sentiments(token_symbol):
    token = Token.objects.get(symbol=token_symbol)
    tweets = fetch_tweets(token_symbol)

    for tweet in tweets:
        sentiment_score = analyze_sentiment(tweet)
        sentiment = Sentiment(token=token, text=tweet, sentiment_score=sentiment_score, source='X (Twitter)')
        sentiment.save()

