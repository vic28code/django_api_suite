from django.urls import path
from .views import LandingAPI

urlpatterns = [
    path('index/', LandingAPI.as_view(), name='landing-index'), 
    path('<str:pk>/', LandingAPI.as_view(), name='landing-api'),
]