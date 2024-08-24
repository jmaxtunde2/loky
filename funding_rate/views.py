# funding/views.py
from django.shortcuts import render
from funding_rate.models import FundingRate
import matplotlib.pyplot as plt
import io
import urllib, base64

def funding_rate_visualization(request):
    rates = FundingRate.objects.all()
    symbols = [rate.symbol for rate in rates]
    funding_rates = [rate.funding_rate for rate in rates]
    sentiment_scores = [rate.sentiment_score for rate in rates]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(symbols, funding_rates, label='Funding Rate')
    plt.plot(symbols, sentiment_scores, label='Sentiment Score', linestyle='--')
    plt.xlabel('Symbol')
    plt.ylabel('Value')
    plt.title('Funding Rate & Sentiment Score')
    plt.legend()
    plt.xticks(rotation=45)

    # Convert plot to PNG image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'funding_rate.html', {'data': uri ,'rates':rates})

