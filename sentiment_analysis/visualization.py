import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import Sentiment
from django.db.models import Avg, Count

def generate_sentiment_trend_chart(token_symbol):
    aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
        .extra({'day': "date(created_at)"}) \
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
            .extra({'day': "date(created_at)"}) \
            .values('day') \
            .annotate(average_sentiment=Avg('sentiment_score'), count=Count('id'))
    elif time_frame == 'hour':
        aggregation = Sentiment.objects.filter(token__symbol=token_symbol) \
            .extra({'hour': "strftime('%Y-%m-%d %H:00:00', created_at)"}) \
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
