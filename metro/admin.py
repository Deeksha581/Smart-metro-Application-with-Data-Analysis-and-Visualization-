from django.contrib import admin
from .models import MetroStation, UserProfile, MetroCard

admin.site.register(MetroStation)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user_id", "full_name", "email", "phone", "has_card")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("has_card",)

@admin.register(MetroCard)
class MetroCardAdmin(admin.ModelAdmin):
    list_display = ("card_number", "user_profile", "balance", "issued_date", "status")
    search_fields = ("card_number", "user_profile__email", "user_profile__full_name")
    list_filter = ("status",)
