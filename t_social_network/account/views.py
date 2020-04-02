from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, Http404
from .forms import LoginForm, UserRegistrationForm, RegistrationPasswordForm
from t_social_network.templates.account.registration_email.subject import subject, EMAIL
from .randomizer import random_char_creator
from django.core.mail import EmailMessage
from django.template.loader import get_template
from .decorators import activate_required
from .models import UserProfileModel
from django.contrib.auth.models import User


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
                    return redirect('account:dashboard')
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


@activate_required
def dasboard(request):
    user = request.user.username
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'user': user})


def user_registration (request):
    template = get_template(EMAIL)
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password_2'])
            if registration_form.pasword_validator() == None:
                return render(request, 'user_registration/wrong_password_page.html')
            registration_password = random_char_creator()
            context = {'registration_password': registration_password,
                        'username': registration_form.cleaned_data['username'], }
            content = template.render(context)
            msg = EmailMessage(subject, content, 'emailrequests1@gmail.com', [registration_form.cleaned_data['email']])
            msg.send()
            new_user.is_active = False
            new_user.save()
            user_profile = UserProfileModel(user=new_user, user_registration_code=registration_password)
            user_profile.save()

            return redirect('account:registration_code',
                            username=registration_form.cleaned_data["username"],
                            number_of_rec=3)

        else:
            return render(request, 'registration/registration_error_page.html',
                                    {'email': registration_form.data['email'],
                                    'name': registration_form.data['username']})
    else:
        return render(request, 'user_registration/user_registration.html', {'form': UserRegistrationForm()})


def user_registration_code_cheacker (request, username, number_of_rec=3):
    if number_of_rec > 3:
        raise Http404("")
    elif number_of_rec <= 0:
        user_object = get_object_or_404(User, username=username)
        user_object.delete()
        content = {'username': user_object.username}
        return render(request, 'account/registration_email/registration_code_error.html', content)
    else:
        form = RegistrationPasswordForm()
        content = {'form': form, 'number_of_rec': number_of_rec}
        if request.method == 'POST':
            form = RegistrationPasswordForm(request.POST)
            if form.is_valid():
                user_object = get_object_or_404(User, username=username)
                profile_user_object = UserProfileModel.objects.get(user__username = username)
                if profile_user_object.user_registration_code == form.cleaned_data['user_registration_code']:
                    user_object.is_active = True
                    user_object.save()
                    login(request, user_object)
                    return redirect('account:dashboard')
                else:
                    number_of_rec -= 1
                    return redirect('account:registration_code',
                                    username=user_object.username,
                                    number_of_rec=number_of_rec)

            else:
                return HttpResponse('Invalid form')

        else:
            return render(request, 'account/registration_email/registration_password_page.html', content)
