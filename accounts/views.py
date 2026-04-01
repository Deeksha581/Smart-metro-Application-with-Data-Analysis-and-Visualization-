import os
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from accounts.utils import import_users_from_excel


# =========================
# PASSWORD VALIDATION RULE
# =========================
PWD_REGEX = re.compile(r"^(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$")


# =========================
# STATIC / COMMON PAGES
# =========================
def about(request):
    return render(request, "accounts/about.html")


def safety(request):
    return render(request, "accounts/safety.html")


def payment(request):
    return render(request, "accounts/payment.html")


def metro_map(request):
    return render(request, "user/map.html")


# =========================
# USER LOGIN
# =========================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("accounts:user_dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("accounts:login")


# =========================
# USER REGISTRATION
# =========================
def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if password != confirm_password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match"}
            )

        if not PWD_REGEX.match(password):
            return render(
                request,
                "accounts/register.html",
                {"error": "Password must be at least 8 characters with 1 number and 1 special character"}
            )

        if User.objects.filter(username=email).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "User already exists with this email"}
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.first_name = full_name[:150]
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if new_password != confirm_password:
            return render(
                request,
                "accounts/forgot_password.html",
                {"error": "Passwords do not match"}
            )

        if not PWD_REGEX.match(new_password):
            return render(
                request,
                "accounts/forgot_password.html",
                {"error": "Password must be at least 8 characters with 1 number and 1 special character"}
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(
                request,
                "accounts/forgot_password.html",
                {"error": "User not found"}
            )

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successful. Please login.")
        return redirect("accounts:login")

    return render(request, "accounts/forgot_password.html")


# =========================
# USER DASHBOARD
# =========================
@login_required
def user_dashboard(request):
    return render(request, "accounts/user_dashboard.html")


# =========================
# ADMIN LOGIN
# =========================
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("accounts:admin_dashboard")

        return render(
            request,
            "accounts/admin_login.html",
            {"error": "Invalid admin credentials"}
        )

    return render(request, "accounts/admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================
@staff_member_required
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")


# =========================
# EXCEL USER IMPORT
# =========================
@login_required
def import_excel_users_view(request):
    excel_path = os.path.join(
        settings.BASE_DIR,
        "static",
        "dataset",
        "namma_metro_dataset_100000.xlsx"
    )

    result = import_users_from_excel(
        excel_path,
        default_password="Metro@123"
    )

    return render(
        request,
        "accounts/import_result.html",
        {"result": result}
    )
