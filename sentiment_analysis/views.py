from django.shortcuts import render
from .models import Token, Sentiment
import matplotlib.pyplot as plt
import io
from django.core.cache import cache
import urllib, base64
from .visualization import generate_sentiment_trend_chart, generate_sentiment_trend_chart_hour

## draw sentiment analysis graph
def plot_sentiments(sentiments):
    dates = [sentiment.date for sentiment in sentiments]
    scores = [sentiment.sentiment_score for sentiment in sentiments]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, scores, marker='o')
    plt.title('Sentiment Scores Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return uri
# Sentiment analysis with Aggregation and Visualization To enhance the sentiment analysis and provide meaningful insight
def aggregate_sentiment_data(request, token_symbol):
    time_frame = request.GET.get('time_frame', 'day')  # Default aggregation by day
    cache_key = f'aggregate_sentiment_{token_symbol}_{time_frame}'
    aggregation = cache.get(cache_key)

    if not aggregation:
        if time_frame == 'day':
            aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
                .extra({'day': "date(created_at)"}) \
                .values('day') \
                .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
        elif time_frame == 'hour':
            aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
                .extra({'hour': "strftime('%Y-%m-%d %H:00:00', created_at)"}) \
                .values('hour') \
                .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
        
        cache.set(cache_key, aggregation, timeout=60*15)  # Cache for 15 minutes

    return aggregation

def sentiment_analyis(request, symbol):
    token = Token.objects.get(symbol=symbol) # get the token Ex: Bitcoin
    sentiments = Sentiment.objects.filter(token=token).order_by('-date') # get sentiment per date
    sentiment_plot = plot_sentiments(sentiments) #graph plot
    chart = generate_sentiment_trend_chart(symbol) # genrate trend graph per day
    time_frame = request.GET.get('time_frame', 'hour')  # Default aggregation per hour
    chart_hour = generate_sentiment_trend_chart_hour(symbol, time_frame) #genrate trend graph per day
    aggregation =  aggregate_sentiment_data(symbol)
    context = {
        'token': token,
        'sentiments': sentiments,
        'sentiment_plot': sentiment_plot,
        'chart' : chart,
        'chart_hour' : chart_hour,
        'aggregation' : aggregation
    }
    return render(request, 'sentiment_analysis.html', context)


