from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from . import forms


@never_cache
def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form_user = form.save()
            raw_password = form.cleaned_data.get('password1')
            # user = User.objects.create_user(username=form_user.username, password=raw_password)

            # login user after signing up
            user = auth.authenticate(username=form_user.username, password=raw_password)
            auth.login(request, user)

            # redirect user to home page
            return redirect('https://skomarov.com')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})
