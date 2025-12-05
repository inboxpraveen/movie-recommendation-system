"""
URL Configuration for Movie Recommendation System
"""
from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    # Main views
    path('', views.main, name='main'),
    
    # API endpoints
    path('api/search/', views.search_movies, name='search_movies'),
    path('api/model-status/', views.model_status, name='model_status'),
    path('api/health/', views.health_check, name='health_check'),
]
