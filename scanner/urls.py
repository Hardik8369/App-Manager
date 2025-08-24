from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # main frontend
    path('scan/', views.scan_directories, name='scan'),  # form submit endpoint
]
