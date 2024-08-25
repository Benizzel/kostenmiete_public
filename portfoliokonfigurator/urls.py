from django.urls import path
from .views import Portfoliokonfiguration

urlpatterns = [
    path('', Portfoliokonfiguration.as_view(), name='portfoliokonfiguration'),
]