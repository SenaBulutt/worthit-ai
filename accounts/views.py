from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

from .forms import RegisterForm


def password_reset_request(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        try:
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            messages.error(request, "Kullanıcı adı veya e-posta hatalı.")
            return redirect("password_reset")

        code = str(random.randint(100000, 999999))

        request.session["reset_email"] = user.email
        request.session["reset_username"] = user.username
        request.session["reset_code"] = code
        request.session["reset_code_time"] = timezone.now().isoformat()
        request.session["reset_verified"] = False

        send_mail(
            "WorthIt AI Şifre Sıfırlama Kodu",
            f"Şifre sıfırlama kodunuz: {code}\nBu kod 3 dakika geçerlidir.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "Doğrulama kodu e-posta adresinize gönderildi.")
        return redirect("verify_code")

    return render(request, "registration/password_reset.html")

def verify_code(request):
    if "reset_code" not in request.session:
        messages.error(request, "Önce e-posta adresinizi girmeniz gerekiyor.")
        return redirect("password_reset")

    if request.method == "POST":
        code = request.POST.get("code")
        saved_code = request.session.get("reset_code")
        code_time = request.session.get("reset_code_time")

        if not code_time:
            messages.error(request, "Kod süresi bulunamadı. Lütfen tekrar kod alın.")
            return redirect("password_reset")

        created_time = timezone.datetime.fromisoformat(code_time)

        if timezone.now() > created_time + timedelta(minutes=3):
            request.session.pop("reset_code", None)
            request.session.pop("reset_code_time", None)
            request.session.pop("reset_verified", None)
            messages.error(request, "Kodun süresi doldu. Lütfen tekrar kod alın.")
            return redirect("password_reset")

        if code == saved_code:
            request.session["reset_verified"] = True
            messages.success(request, "Kod doğrulandı. Yeni şifrenizi belirleyebilirsiniz.")
            return redirect("new_password")

        messages.error(request, "Kod hatalı.")
        return redirect("verify_code")

    return render(request, "registration/verify_code.html")


def new_password(request):
    if not request.session.get("reset_verified"):
        messages.error(request, "Önce doğrulama kodunu onaylamanız gerekiyor.")
        return redirect("verify_code")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Parolalar eşleşmiyor.")
            return redirect("new_password")

        email = request.session.get("reset_email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Kullanıcı bulunamadı.")
            return redirect("password_reset")

        user.password = make_password(password1)
        user.save()

        request.session.pop("reset_email", None)
        request.session.pop("reset_code", None)
        request.session.pop("reset_code_time", None)
        request.session.pop("reset_verified", None)

        messages.success(request, "Şifreniz başarıyla güncellendi.")
        return redirect("login")

    return render(request, "registration/new_password.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})