from django.urls import path, include
from . import views

# app_name = 'predict'

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('results/', views.results, name='results'),
]
