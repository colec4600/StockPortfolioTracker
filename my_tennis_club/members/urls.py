from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search_results, name='search'),
    path('see_stock/', views.see_stock, name='see_stock'),
    path('add_stock/', views.add_stock, name='add_stock'),
]