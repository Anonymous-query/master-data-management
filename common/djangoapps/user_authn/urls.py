from django.urls import include, path

from .views import login, login_and_registration

urlpatterns = [
    path('login', login_and_registration.login_form, name='signin_user'),
    path('register', login_and_registration.registration_form, name='register_user'),
]