from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm
from .randomizer import random_char_creator
# Create your views here.

def user_login (request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Successful authorization')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid authorization')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form, 'title': 'login page'})


def user_logout(request):
    logout(request)
    return redirect('account:login')

@login_required
def dasboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_registration (request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password_2'])
            if registration_form.pasword_validator() == None:
                return render(request, 'user_registration/wrong_password_page.html')
            new_user.save()
            return redirect('account:dashboard')
        else:
            return render(request, 'registration/registration_error_page.html',
                                                                        {'email': registration_form.data['email'],
                                                                        'name': registration_form.data['username']})
    else:
        return render(request, 'user_registration/user_registration.html', {'form': UserRegistrationForm()})
