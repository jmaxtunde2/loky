from django.urls import path
from . import views

urlpatterns = [
    path('token/<str:symbol>/', views.sentiment_analyis, name='sentiment_analysis'),
     path('token_search/', views.token_search, name='token_search'),
]