
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('sentiment/', include('sentiment_analysis.urls')),
    path('detect/', include('anomaly_detection.urls')),
    path('analysis/', include('token_analysis.urls')),
    path('users/', include('users.urls')), 
    path('users/', include('django.contrib.auth.urls')), 
    path('', include('pages.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    #re_path("accounts/", include("allauth.urls")),
]


#clientID: 548803931696-h00dk397u65ib9mjl15ikadlmshfo2vt.apps.googleusercontent.com
#secret: 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