from django.urls import path
from .views import HomePageView,AboutPageView,DonatePageView
from .views import advertise

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about-loky', AboutPageView.as_view(), name='about'),
    path('donate-loky', DonatePageView.as_view(), name='donate'),
    path('advertise/', advertise, name='advertise'),
]