from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', obtain_auth_token),
    path('logout/', views.logout),
]
