from django.contrib import admin
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import path
from django.urls import include


def home(request):
    return redirect(static('index.html')) # serves the SPA from the static dir

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('simpleauth.urls')),
    path('api/v1/', include('api.urls')),
    path('/', home, name="home"),
]
