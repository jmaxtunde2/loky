from django.shortcuts import render
from .models import Token, Sentiment, BitcoinSentiment
import matplotlib.pyplot as plt
import io
from io import BytesIO
from django.core.cache import cache
import urllib, base64
from django.db.models import Avg, Count, F
from django.db.models.functions import TruncDate, TruncHour
#from .visualization import generate_sentiment_trend_chart, generate_sentiment_trend_chart_hour
from django.http import JsonResponse

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
                .annotate(day=TruncDate('created_at')) \
                .values('day') \
                .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
        elif time_frame == 'hour':
            aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
                .annotate(hour=TruncHour('created_at')) \
                .values('hour') \
                .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
        
        cache.set(cache_key, aggregation, timeout=60*15)  # Cache for 15 minutes

    return aggregation

def generate_sentiment_trend_chart(token_symbol):
    aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
        .annotate(day=TruncDate('created_at')) \
        .values('day') \
        .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))

    days = [entry['day'] for entry in aggregation]
    sentiment_scores = [entry['average_sentiment'] for entry in aggregation]

    plt.figure(figsize=(10, 5))
    plt.plot(days, sentiment_scores, marker='o')
    plt.title(f'Sentiment Trend for {token_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return graph




def generate_sentiment_trend_chart_hour(token_symbol, time_frame='day'):
    if time_frame == 'day':
        aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
            .annotate(day=TruncDate('created_at')) \
            .values('day') \
            .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
    elif time_frame == 'hour':
        aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
            .annotate(hour=TruncHour('created_at')) \
            .values('hour') \
            .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))

    time_points = [entry['day'] if time_frame == 'day' else entry['hour'] for entry in aggregation]
    sentiment_scores = [entry['average_sentiment'] for entry in aggregation]

    plt.figure(figsize=(10, 5))
    plt.plot(time_points, sentiment_scores, marker='o')
    plt.title(f'Sentiment Trend for {token_symbol}')
    plt.xlabel('Date' if time_frame == 'day' else 'Hour')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return graph

def sentiment_analyis(request, symbol):
    token = Token.objects.get(symbol=symbol) # get the token Ex: Bitcoin
    sentiments = Sentiment.objects.filter(token=token).order_by('-date') # get sentiment per date
    sentiment_plot = plot_sentiments(sentiments) #graph plot
    chart = generate_sentiment_trend_chart(symbol) # genrate trend graph per day
    time_frame = request.GET.get('time_frame', 'hour')  # Default aggregation per hour
    chart_hour = generate_sentiment_trend_chart_hour(symbol, time_frame) #genrate trend graph per day
    aggregation =  aggregate_sentiment_data(request, symbol)
    context = {
        'token': token,
        'sentiments': sentiments,
        'sentiment_plot': sentiment_plot,
        'chart' : chart,
        'chart_hour' : chart_hour,
        'aggregation' : aggregation
    }
    return render(request, 'sentiment_analysis.html', context)

def token_search(request):
    query = request.GET.get('query', '')
    if query:
        tokens = Token.objects.filter(name__icontains=query)[:6]
        results = [{'name': token.name, 'symbol': token.symbol} for token in tokens]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def bitcoin_sentiment_view(request):
    # Fetch sentiments in descending order by date
    sentiments = BitcoinSentiment.objects.all().order_by('-date')

    dates = [s.date for s in sentiments]
    prices = [s.price for s in sentiments]
    means = [s.mean for s in sentiments]

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, label='Price', color='blue')
    plt.plot(dates, means, label='Mean Sentiment', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Bitcoin Sentiment and Price Over Time')
    plt.legend()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    image_b64 = base64.b64encode(image_png).decode('utf-8')

    # Render the template with the chart and sentiment data
    return render(request, 'bitcoin_sentiment.html', {
        'chart': image_b64,
        'sentiments': sentiments,
    })
