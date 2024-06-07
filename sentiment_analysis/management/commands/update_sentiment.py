from django.core.management.base import BaseCommand
from sentiment_analysis.models import Token
from sentiment_analysis.sentiment import save_sentiments

class Command(BaseCommand):
    help = 'Update sentiment data for tokens'

    def handle(self, *args, **kwargs):
        tokens = Token.objects.all()
        for token in tokens:
            save_sentiments(token.symbol)
            self.stdout.write(self.style.SUCCESS(f'Successfully updated sentiment data for {token.symbol}'))