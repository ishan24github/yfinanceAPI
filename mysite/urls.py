from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('stock/<str:pk>', views.stock, name="stock"),
    path('search', views.search, name="search"),
    path('get/stock', views.loadstock, name = "loadstock"),
]