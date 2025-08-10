from django.urls import path
from .views import LandingAPI, LandingAPIItem

urlpatterns = [
    path('index/', LandingAPI.as_view(), name='landing-index'), 
    path('<str:pk>/', LandingAPI.as_view(), name='landing-api'),
    path('item/<str:item_id>/', LandingAPIItem.as_view(), name='landing-item-detail'),
]