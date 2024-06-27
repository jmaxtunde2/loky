from django.shortcuts import render, get_object_or_404
from django.conf import settings
import os
from anomaly_detection.models import Anomaly, RiskAssessment

def anomaly_list(request):
    anomaly_images = []
    anomaly_dir = os.path.join(settings.BASE_DIR, 'static', 'anomaly')
    if os.path.exists(anomaly_dir):
        for filename in os.listdir(anomaly_dir):
            if filename.endswith('.png'):
                anomaly_images.append(f'anomaly/{filename}')
    return render(request, 'anomaly_list.html', {'images': anomaly_images})

def anomaly_detail(request, crypto_id):
    anomalies = Anomaly.objects.filter(crypto_id=crypto_id)
    anomaly_image = f'anomaly/anomalies_{crypto_id}.png'
    image_path = os.path.join(settings.BASE_DIR, 'static', anomaly_image)
    image_exists = os.path.exists(image_path)
    return render(request, 'anomaly_detail.html', {'anomalies': anomalies, 'image': anomaly_image if image_exists else None})

def risk_assessment(request):
    risk_assessments = RiskAssessment.objects.all()
    return render(request, 'risk_assessment.html', {'risk_assessments': risk_assessments})

def risk_assessment_detail(request, crypto_id):
    risk = get_object_or_404(RiskAssessment, crypto_id=crypto_id)
    risk_image = f'anomaly/risk_assessment_{crypto_id}.png'
    image_path = os.path.join(settings.BASE_DIR, 'static', risk_image)
    image_exists = os.path.exists(image_path)
    return render(request, 'risk_assessment_detail.html', {'risk': risk, 'image': risk_image if image_exists else None})
