
from django.urls import path
from . import views

urlpatterns = [
    path('anomalies/', views.anomaly_list, name='anomaly_list'),
    path('anomalies/<str:crypto_id>/', views.anomaly_detail, name='anomaly_detail'),
    path('risk-assessment/', views.risk_assessment, name='risk_assessment'),
    path('risk-assessment/<str:crypto_id>/', views.risk_assessment_detail, name='risk_assessment_detail'),
]


