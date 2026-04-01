from django.db import models
from django.contrib.auth.models import User
class MetroStation(models.Model):
    LINE_CHOICES = [
        ('Purple', 'Purple Line'),
        ('Green', 'Green Line'),
        ('Yellow', 'Yellow Line'),
    ]

    name = models.CharField(max_length=100)
    line = models.CharField(max_length=20, choices=LINE_CHOICES)
    code = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    platforms = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.line})"

class UserProfile(models.Model):
    user_id = models.IntegerField(unique=True)  # from Excel
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)      # KEY to link login user
    has_card = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class MetroCard(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="metro_card")
    card_number = models.CharField(max_length=20, unique=True)
    balance = models.IntegerField(default=0)
    issued_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="ACTIVE")

    def __str__(self):
        return f"{self.card_number} - {self.user_profile.full_name}"

