from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('texts/', views.texts),
    path('skips/', views.skips),
    path('speeches/', views.speeches),
    path('user/', views.user),
    path('register/', views.register),
    path('login/', views.login)
]
