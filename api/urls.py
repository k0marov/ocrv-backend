from django.urls import path
from . import views


urlpatterns = [
    path('texts/', views.get_texts),
    path('skips/', views.skips),
    path('speeches/', views.post_speech),
]
