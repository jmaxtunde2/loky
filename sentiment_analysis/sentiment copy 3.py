import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from .models import Token, Sentiment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

import re
import json
# Twitter scraping setup
# def fetch_tweets(token_symbol):
#     url = f'https://x.com/search?q=%{token_symbol}&src=typed_query'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     tweets = [p.text for p in soup.find_all('p', {'class': 'tweet-text'})]
#     return tweets[:100]

def fetch_tweets(token_symbol, count=100):
    # Setup the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--remote-debugging-port=9222')  # Enable remote debugging

    # Ensure compatible ChromeDriver is installed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://twitter.com/search?q=%23{token_symbol}&src=typed_query"
    driver.get(url)

    # Scroll down to load tweets
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(5):  # Adjust the range to load more tweets if needed
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)  # Adjust the sleep time if needed

    # Collect tweet texts
    tweets = []
    tweet_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
    for tweet in tweet_elements[:count]:
        tweets.append(tweet.text)

    driver.quit()
    return tweets

# Reddit scraping setup
# def fetch_reddit_posts(token_symbol):
#     url = f'https://www.reddit.com/search/?q={token_symbol}'
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     posts = [div.text for div in soup.find_all('div', {'class': 'scrollerItem'})]
#     return posts[:100]

# # Altcoinstalks scraping setup
# def fetch_altcoinstalks_posts(token_symbol):
#     url = f'https://www.altcoinstalks.com/index.php?topic={token_symbol}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         posts = soup.find_all('div', class_='post')
#         return [post.get_text() for post in posts]
#     return []

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
        # 'Reddit': fetch_reddit_posts,
        # 'Altcoinstalks': fetch_altcoinstalks_posts,
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


