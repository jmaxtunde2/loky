from django.db import models

#creating a model for our cryptocurrencies (BTC, Eth,..)
class Token(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)
    circulating_supply = models.DecimalField(max_digits=20, decimal_places=2)
    max_supply = models.DecimalField(max_digits=20, decimal_places=2)
    logo = models.URLField(max_length=200, blank=True, null=True)  
    crypto_id = models.CharField(max_length=100, unique=True, default='unknown') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f'{self.name} ({self.symbol})'

#creating a model to store the sentiment of each token
class Sentiment(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    text = models.TextField()
    sentiment_score = models.FloatField()
    source = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Sentiment for {self.token.name} from {self.source}'

class BitcoinSentiment(models.Model):
    date = models.DateField(unique=True)
    price = models.FloatField()
    volume = models.FloatField()
    score1 = models.FloatField()
    score2 = models.FloatField()
    score3 = models.FloatField()
    sum = models.FloatField()
    mean = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return f"Sentiment on {self.date}"