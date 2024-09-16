from django.urls import include, path, re_path

from .views import login, login_and_registration, logout

urlpatterns = [
    path('login', login_and_registration.login_form, name='signin_user'),
    path('register', login_and_registration.registration_form, name='register_user'),
    path('login_ajax', login.login_user, name="login_user"),
    re_path(
        r'^api/user/account/login_session/$',
        login.LoginSessionView.as_view(),
        name="user_api_login_session"
    ),
    # auth_backends logout view.
    path('logout', logout.LogoutView.as_view(), name='logout'),
]