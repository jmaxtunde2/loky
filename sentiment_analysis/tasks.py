# sentiment_analysis/tasks.py

from celery import shared_task
from .models import Token
from .sentiment import save_sentiments

@shared_task
def update_sentiments_task():
    tokens = Token.objects.all()
    for token in tokens:
        save_sentiments(token.symbol)
