
# api/health/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('db/', views.database_check, name='database_check'),
]
