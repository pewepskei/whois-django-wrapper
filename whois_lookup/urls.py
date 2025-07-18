from django.urls import path
from .views import WhoisLookupAPIView

urlpatterns = [
    path('whois-lookup', WhoisLookupAPIView.as_view(), name='api_whois_lookup'),
]
