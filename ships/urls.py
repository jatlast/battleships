from django.urls import path
from . import views

urlpatterns = [
    path('', views.ship_list, name='ship_list'),
    path('ships/<str:shipname>/', views.ship_detail, name='ship_detail'),
]
