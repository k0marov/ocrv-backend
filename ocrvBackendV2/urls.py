from django.contrib import admin
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import path, reverse_lazy
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authapi.urls')),
    path('api/v1/', include('api.urls')),
]
