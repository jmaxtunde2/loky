from django.core.management.base import BaseCommand
from sentiment_analysis.sentiment import save_sentiments
from sentiment_analysis.models import Token

class Command(BaseCommand):
    help = 'Update sentiment data for tokens'

    def handle(self, *args, **options):
        tokens = Token.objects.values_list('symbol', flat=True).distinct()
        for token_symbol in tokens:
            save_sentiments(token_symbol)
            self.stdout.write(self.style.SUCCESS(f'Successfully updated sentiment for token symbol {token_symbol}'))
