# urlshortener/urls.py
from django.urls import path
from .views import ShortenURLView, RedirectOriginalURLView

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten_url'),
    path('redirect/<str:short_code>/', RedirectOriginalURLView.as_view(), name='redirect_original_url'),
]
