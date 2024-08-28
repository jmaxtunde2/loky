
from django.urls import path
from . import views

urlpatterns = [
    path('visualization/', views.funding_rate_visualization, name='funding_rate'),
]