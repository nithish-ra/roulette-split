from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save-split/', views.save_split, name='save_split'),
    path('dashboard/', views.dashboard, name='dashboard'),
]