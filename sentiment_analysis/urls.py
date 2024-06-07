from django.urls import path
from . import views

urlpatterns = [
    path('token/<str:symbol>/', views.sentiment_analyis, name='sentiment_analysis'),
]