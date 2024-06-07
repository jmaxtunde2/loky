from django.contrib import admin
from .models import Token,Sentiment

#admin.site.register(Token)
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'market_cap', 'price', 'volume_24h', 'circulating_supply', 'max_supply', 'logo')
    search_fields = ('name', 'symbol')

#admin.site.register(Sentiment)
@admin.register(Sentiment)
class SentimentAdmin(admin.ModelAdmin):
    list_display = ('token', 'sentiment_score', 'source', 'date')
    search_fields = ('token', 'source')
