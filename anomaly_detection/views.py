# views.py
from django.shortcuts import render, get_object_or_404
from anomaly_detection.models import Anomaly
import os

def anomaly_list(request):
    anomalies = Anomaly.objects.filter(is_anomaly=True).distinct('crypto_id')
    images = [f'anomaly/anomalies_{anomaly.crypto_id}.png' for anomaly in anomalies]
    context = {'images': images}
    return render(request, 'anomaly_list.html', context)

def anomaly_detail(request, crypto_id):
    anomaly = get_object_or_404(Anomaly, crypto_id=crypto_id, is_anomaly=True)
    image = f'anomaly/anomalies_{crypto_id}.png'
    context = {'image': image, 'crypto_id': crypto_id}
    return render(request, 'anomaly_detail.html', context)
