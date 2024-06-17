from django.urls import path
from . import views

urlpatterns = [
    path('token-analysis/<str:symbol>/', views.token_analyis, name='token_analyis'),
     path('feature-analysis/', views.analyze_token, name='analyze_token'),
]