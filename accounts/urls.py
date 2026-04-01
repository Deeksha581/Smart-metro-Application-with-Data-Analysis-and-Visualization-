from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [

    # =====================
    # USER AUTHENTICATION
    # =====================
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),

    path(
        "register/",
        views.user_register,
        name="register"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

    # =====================
    # USER DASHBOARD
    # =====================
    path(
        "user-dashboard/",
        views.user_dashboard,
        name="user_dashboard"
    ),

    # =====================
    # STATIC / INFO PAGES
    # =====================
    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "safety/",
        views.safety,
        name="safety"
    ),

    path(
        "payment/",
        views.payment,
        name="payment"
    ),

    path(
        "metro-map/",
        views.metro_map,
        name="metro_map"
    ),

    # =====================
    # ADMIN
    # =====================
    path(
        "admin-login/",
        views.admin_login,
        name="admin_login"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # =====================
    # EXCEL IMPORT
    # =====================
    path(
        "import-users/",
        views.import_excel_users_view,
        name="import_users"
    ),
]
