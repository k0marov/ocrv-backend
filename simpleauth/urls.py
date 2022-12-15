from django.contrib.auth import views as auth_views
from django.urls import path, reverse, reverse_lazy

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html", next_page=reverse_lazy('home')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('signup/', views.signup, name='signup'),
]