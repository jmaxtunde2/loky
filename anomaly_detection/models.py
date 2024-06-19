# models.py
from django.db import models

class Anomaly(models.Model):
    crypto_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    price = models.FloatField()
    volume = models.FloatField()
    is_anomaly = models.BooleanField()
