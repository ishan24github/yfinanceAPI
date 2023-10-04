from django.urls import path
from mysite import views

urlpatterns = [
    path('',views.index, name='index'),
    path('stock/<str:pk>', views.stock, name="stock"),
    path('search', views.search, name="search"),
    path('get/stock', views.loadstock, name = "loadstock"),
    path('login', views.loginPage , name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register',views.registerPage, name='register')
]

