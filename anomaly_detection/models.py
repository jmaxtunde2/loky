# models.py
from django.db import models

class Anomaly(models.Model):
    crypto_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    price = models.FloatField()
    volume = models.FloatField()
    is_anomaly = models.BooleanField()

    class Meta:
        unique_together = ('crypto_id', 'timestamp')

class RiskAssessment(models.Model):
    crypto_id = models.CharField(max_length=100, unique=True)
    volatility = models.FloatField()
    liquidity = models.FloatField()
    anomaly_count = models.IntegerField()

# from django.db import models

# class Anomaly(models.Model):
#     crypto_id = models.CharField(max_length=100)
#     timestamp = models.DateTimeField()
#     price = models.FloatField()
#     volume = models.FloatField()
#     is_anomaly = models.BooleanField()
#     market_cap = models.FloatField(null=True, blank=True)
#     volatility = models.FloatField(null=True, blank=True)
#     liquidity = models.FloatField(null=True, blank=True)
#     regulatory_risk = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f'{self.crypto_id} ({self.price})'
