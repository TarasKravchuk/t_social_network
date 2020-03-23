from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetConfirmView,\
    PasswordResetDoneView, PasswordResetView

app_name = 'account'

urlpatterns = [
    path('', dasboard, name='dashboard'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html',
                                                      email_template_name='registration/password_reset_email.html',
                                                      subject_template_name='registration/password_reset_subject.txt',
                                                      title='Password reset for your account "t_social_network"',
                                                      success_url=reverse_lazy('account:password_reset_done')),
                                                      name='password_reset'),


    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
                                                               name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_change/', PasswordChangeView.as_view(), name='password_change'),

    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
                                                                name='password_reset_complete'),

    path('registration/', user_registration, name='registration'),
]
