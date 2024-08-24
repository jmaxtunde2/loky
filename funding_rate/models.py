
# funding_rate/models.py
from django.db import models

class FundingRate(models.Model):
    coin_name = models.CharField(max_length=100)
    stablecoin = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50, unique=True)
    funding_rate = models.FloatField()
    exchange = models.CharField(max_length=100)
    sentiment_score = models.FloatField()  # This can be calculated based on the funding rate
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coin_name} ({self.symbol}) - Rate: {self.funding_rate}"
