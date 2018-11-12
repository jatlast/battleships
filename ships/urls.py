from django.urls import path
from . import views

urlpatterns = [
    path('', views.ship_list, name='ship_list'),
#    path('ships/error', views.error_page, name='error_page'),
    path('ships/<str:shipname>/', views.ship_detail, name='ship_detail'),
    path('ships/new', views.ship_new, name='ship_new'),
    path('ships/<str:shipname>/edit/', views.ship_edit, name='ship_edit'),
]
