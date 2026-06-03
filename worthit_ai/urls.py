from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("finance.urls")),
    path(
    "password-reset/",
    auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html"
    ),
    name="password_reset"
),

path(
    "password-reset/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),
    name="password_reset_done"
),
path(
    "verify-code/",
    auth_views.TemplateView.as_view(
        template_name="registration/verify_code.html"
    ),
    name="verify_code"
),

path(
    "new-password/",
    auth_views.TemplateView.as_view(
        template_name="registration/new_password.html"
    ),
    name="new_password"
),
]