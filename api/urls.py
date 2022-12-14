from django.urls import path
from . import views


urlpatterns = [
    path('text/', views.texts),
    path('skips/', views.skips),
    path('speeches/', views.speeches),
]
