from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('get_nearest_station/', views.get_nearest_station, name='get_nearest_station'),
    path('get_sacco_info/', views.get_sacco_info, name='get_sacco_info'),
]