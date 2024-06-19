
from django.urls import path
from . import views

urlpatterns = [
    path('anomalies/', views.anomaly_list, name='anomaly_list'),
    path('anomalies/<str:crypto_id>/', views.anomaly_detail, name='anomaly_detail'),
]


