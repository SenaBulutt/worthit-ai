from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, password_reset_request, verify_code, new_password

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("password-reset/", password_reset_request, name="password_reset"),
    path("verify-code/", verify_code, name="verify_code"),
    path("new-password/", new_password, name="new_password"),
]