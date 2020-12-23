from django.urls import path
from . import views
from users.forms import LoginForm 


urlpatterns = [
    path('', views.welcome),
    path('register', views.register),
    path('login/', views.login),
    path('logout', views.logout),
    path('configure', views.update_profile,name='configure')
]