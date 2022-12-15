from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache

from . import forms


@never_cache
def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form_user = form.save()
            auth.login(request, form_user)

            return redirect(reverse_lazy('home'))
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})
