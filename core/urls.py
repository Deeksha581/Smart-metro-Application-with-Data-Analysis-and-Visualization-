from django.contrib import admin
from django.urls import path, include
from .views import home, about
from core.views import home

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),   # ✅ ADD THIS
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("metro/", include("metro.urls")),
    path("analytics/", include("analytics.urls")),

]